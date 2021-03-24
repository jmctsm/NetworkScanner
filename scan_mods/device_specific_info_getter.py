#!python

"""
This will be used to get specific info from a device that is using Cisco IOS
It will use netmiko and NTC-Templates to return all information via JSON
"""

import os
import sys
from typing import Type

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

os.environ[
    "NTC_TEMPLATES_DIR"
] = f"{grandparentdir}\\NTC_Templates\\ntc-templates\\ntc_templates\\templates\\"


from scan_mods.common_validation_checks.check_address import check_address
from scan_mods.common_validation_checks.check_username import check_username
from scan_mods.common_validation_checks.check_password import check_password
from scan_mods.common_validation_checks.check_enable_password import (
    check_enable_password,
)

import time
import json
import netmiko
import textfsm


def check_device_type(device_type, address):
    """
    Validate that the device type will return the correct string for NetMiko
    Args:
        device_type (str) : string of device types
        address (str): string of the IP address
    return:
        str : string of the device type to use with NetMiko
    """
    if device_type is None:
        raise ValueError(
            f"You did not enter a device type to search for at address {address}.  Try again"
        )
    if device_type is not None:
        if isinstance(device_type, str):
            if device_type == "ios":
                return ("cisco_ios", "cisco_ios")
            elif device_type == "nxos_ssh":
                return ("cisco_nxos_ssh", "cisco_nxos")
            elif device_type == "iosxr":
                return ("cisco_xr", "cisco_xr")
            elif device_type == "linux":
                return ("linux_ssh", "linux")
            else:
                raise ValueError(
                    f"Device Type of {device_type} is not known.  Try again."
                )
        else:
            raise TypeError(
                f"You did not enter a string for the device type at address {address}.  Try again"
            )


def device_info_getter(
    address=None,
    username=None,
    password=None,
    device_type=None,
    enable_password_needed=False,
    enable_password=None,
    port_to_use=22,
):
    """
    Will connect to a device using netmiko and pull information from the device
    and format it using TEXTFSM settings into JSON for output later
    """
    if address is None:
        raise ValueError(f"You did not tell me what to connect to Fix This")
    valid_address = check_address(address)
    valid_username = check_username(username, valid_address)
    valid_password = check_password(password, valid_address)
    valid_device_type, valid_textfsm_string = check_device_type(
        device_type, valid_address
    )
    if enable_password_needed:
        valid_enable_password = check_enable_password(enable_password, valid_address)
    if port_to_use != 22:
        if isinstance(port_to_use, int):
            if port_to_use > 0 and port_to_use < 65535:
                connect_port = port_to_use
            else:
                print(f"You gave me a non-valid port.  Connecting on port 22.")
                connect_port = 22
        else:
            print(f"You gave me a non-valid port.  Connecting on port 22.")
            connect_port = 22
    else:
        connect_port = 22
    if enable_password_needed:
        device_parameters = {
            "device_type": valid_device_type,
            "host": valid_address,
            "username": valid_username,
            "password": valid_password,
            "port": connect_port,
            "secret": valid_enable_password,
        }
    else:
        device_parameters = {
            "device_type": valid_device_type,
            "host": valid_address,
            "username": valid_username,
            "password": valid_password,
            "port": connect_port,
        }

    output_dict = {}
    print(
        f"Attempting connection to {valid_address} to get device specific information"
    )
    try:
        device_connection = netmiko.ConnectHandler(**device_parameters)
    except netmiko.ssh_exception.NetmikoTimeoutException:
        output_dict["ERROR"] = {
            "NetmikoTimeoutException": f"Device Connection Timed Out for {valid_address}"
        }
        return output_dict
    except netmiko.ssh_exception.NetmikoAuthenticationException:
        output_dict["ERROR"] = {
            "NetmikoAuthenticationException": f"Authentication failed for {valid_address}"
        }
        return output_dict
    except Exception as ex:
        print(ex)
        raise
    command_dict = find_commands(valid_textfsm_string)
    print(f"Sending commands to {valid_address} for device specific information")
    for command_key, command_value in command_dict.items():
        try:
            output_string = device_connection.send_command(
                command_value, use_textfsm=True
            )
        except textfsm.parser.TextFSMError:
            output_string = "% Invalid input detected "
        except OSError:
            output_string = "% Invalid input detected "
        except netmiko.ssh_exception.NetmikoTimeoutException:
            output_string = "Timed-out reading channel, data not available."
        except Exception as ex:
            print(ex)
            output_string = "% Invalid input detected "
            raise
        if (
            "% Invalid input detected " in output_string
            or "% Incomplete command" in output_string
        ):
            continue
        output_dict[command_key] = output_string
    return output_dict


def find_commands(device_type):
    """
    This will read through the list of available commands in the NTC templates and will return a list of comands available for the device type
    Args:
        device_type (str) : string of the device_type to look for in the NTC templates

    Return:
        dict : dict of commands for the device type where key is the command name with underscores and value is the command
    """
    if not isinstance(device_type, str):
        raise TypeError(
            f"Device Type should be a string.  Not {type(device_type).__name__}"
        )
    commands_found = {}
    print(f"Grabbing all commands for device type {device_type}")
    for template_name in os.listdir(
        f"{parentdir}\\NTC_Templates\\ntc-templates\\ntc_templates\\templates\\"
    ):
        if device_type in template_name:
            command_name = template_name[len(device_type) + 1 : -8]
            command_value = " ".join(command_name.split("_"))
            commands_found[command_name] = command_value
    return commands_found


if __name__ == "__main__":
    start_time = time.time()
    cisco_iosxe_no_en = {"192.168.89.254": "ios"}
    cisco_iosv_enable = {"192.168.89.253": "ios"}
    cisco_iosl2_no_enable = {"192.168.89.252": "ios"}
    cisco_iosxe_enable = {"192.168.89.247": "ios"}
    cisco_nx0s7 = {"192.168.89.251": "nxos_ssh"}
    linux_ubuntu_server = {"192.168.89.80": "linux"}

    username = "jmctsm"
    password = "ciscocisco"
    enable_password = None
    no_enable_device_list = [
        cisco_iosxe_no_en,
        cisco_iosl2_no_enable,
        cisco_nx0s7,
        linux_ubuntu_server,
    ]
    enable_device_list = [
        cisco_iosv_enable,
        cisco_iosxe_enable,
    ]
    json_input_dict = {}
    for device in no_enable_device_list:
        for device_ip, device_type in device.items():
            device_info = device_info_getter(
                address=device_ip,
                username=username,
                password=password,
                device_type=device_type,
                enable_password_needed=False,
            )
            json_input_dict[device_ip] = device_info

    enable_password = "ciscocisco"

    for device in enable_device_list:
        for device_ip, device_type in device.items():
            device_info = device_info_getter(
                address=device_ip,
                username=username,
                password=password,
                device_type=device_type,
                enable_password_needed=True,
                enable_password=enable_password,
            )
            json_input_dict[device_ip] = device_info

    print(json_input_dict)
    json_output = json.dumps(json_input_dict, indent=4)
    print("\n\n\n\n")
    print(json_output)
    with open(f"Output\\test_output_{time.time()}.txt", "w") as file_output:
        file_output.write(json_output)
    duration = time.time() - start_time
    print(f"Duration to run was {duration}")
