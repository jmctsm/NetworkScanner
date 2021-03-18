#!python

"""
This will connect to a device that is Cisco and attempt to get the config from that device
"""

import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from typing import Type
from scan_mods.device_class import FoundDevice
from scan_mods.common_validation_checks.check_address import check_address
from scan_mods.common_validation_checks.check_username import check_username
from scan_mods.common_validation_checks.check_password import check_password
from scan_mods.common_validation_checks.check_enable_password import (
    check_enable_password,
)
import ipaddress
import time
import getpass
import napalm
import paramiko
import json
import datetime


def check_ports(port_dictionary):
    """
    This will run through the ports that are supposedly open and see if 22 is listed.  If so, it will return the device type if it can be determined
    or False if not open
    Args:
        port_dictionary (dict) : dictionary of either one port or multiple ports of format {<port_number>:<header>}
    Return
        False : if 22 or SSH is not in the list
        string : device type or unknown from header information
        int : port number that ssh is running on
    """
    if not isinstance(port_dictionary, dict):
        raise TypeError(
            f"Port dictionary passed was of type {type(port_dictionary).__name__}.  It needs to be a dictionary"
        )
    for key, value in port_dictionary.items():
        if not isinstance(key, str):
            try:
                key = str(key)
            except Exception as ex:
                print(
                    f"Port could not be made into a string.  It was a type of {type(key).__name__}"
                )
                print(ex)
                raise
        if not isinstance(value, dict):
            raise TypeError(
                f"The Port value was not a dict.  It was a type of {type(value).__name__}"
            )
        if key == "22":
            for key, value in port_dictionary[key].items():
                if key == "ERROR":
                    continue
                if "Cisco" in value:
                    return (22, "Cisco")
                # This can be expanded as more and more are learned
                elif "Ubuntu" in value:
                    return (22, "Linux")
                else:
                    return (22, "Other")
        for value in port_dictionary[key].values():
            if "SSH" in value:
                return (int(key), "Other")

    return (False, False)


def get_device_type(address, port, username, password, enable_password, header):
    """
    Will attempt to connect to a device and determine the device type for napalm
    Args:
        address (str) : string of the IP to connect to
        port (int) : integer of the port connecting to
        username (str): string of the username
        password (str): string of the password
        enable_password (str): string of the enable password
        open (str): string of the type device is thought to be
    return:
        str : string of either device type known or if it is unknown.  Types will be used for napalm
    """
    for item in [address, username, password, header]:
        if not isinstance(item, str):
            raise TypeError(f"{item} is not a string.  It is a {type(item).__name__}")
    try:
        ipaddress.IPv4Address(address)
    except ipaddress.AddressValueError:
        raise ipaddress.AddressValueError(
            f"{address} is not set up to be an IPv4 adddress."
        )
    if not isinstance(port, int):
        raise TypeError(f"{port} is not a string.  It is a {type(port).__name__}")
    if port < 0 or port > 65535:
        raise ValueError(f"Port number needs to be between 0 and 65535")
    if enable_password is not None and not isinstance(enable_password, str):
        raise TypeError(
            f"{enable_password} is not a string.  It is a {type(port).__name__}"
        )

    ssh_open = paramiko.SSHClient()
    ssh_open.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Attempting connection to {address}")
    try:
        # to work for Cisco added in the look_for_keys and allow_agent parameters
        ssh_open.connect(
            address, port, username, password, look_for_keys=False, allow_agent=False
        )
    except paramiko.AuthenticationException:
        return_dict = {
            "Version Info": f"[ERROR] paramiko.AuthenticationException: Authentication failed for device {address}"
        }
        return return_dict
    except TimeoutError:
        return_dict = {
            "Version Info": f"[ERROR] TimeoutError: Connection timed out for device {address}"
        }
        return return_dict
    if header == "Cisco":
        if enable_password is None:
            stdin_lines, stdout_lines, stderr_lines = ssh_open.exec_command(
                "show version"
            )
            if stderr_lines.readlines():
                raise ValueError(f"Something happened when connecting to {address}")
            output_list = []
            for line in stdout_lines.readlines():
                if line.strip() == "":
                    continue
                output_list.append(line.strip())
        elif enable_password is not None:
            # this means we have to invoke a shell and start issuing commands :)
            shell_connection = ssh_open.invoke_shell()
            shell_connection.send("enable\n")
            time.sleep(0.5)
            shell_connection.send(f"{enable_password}\n")
            time.sleep(0.5)
            shell_connection.send("term length 0\n")
            time.sleep(0.5)
            output_bytes = shell_connection.recv(65535)
            shell_connection.send("show version\n")
            time.sleep(0.5)
            output_bytes = shell_connection.recv(65535)
            output_list = []
            temp_list = output_bytes.decode("utf-8").splitlines()
            for item in temp_list:
                if item == "":
                    continue
                output_list.append(item)
        else:
            raise ValueError(
                f"Enable password parameter has something jacked up with it.  enable_password = {enable_password}"
            )

        return_dict = {"Version Info": output_list}
        return_dict["OS Type"] = "unknown"
        for line in output_list:
            if "IOS-XE" in line:
                return_dict["OS Type"] = "ios"
                break
            elif "IOS-XE" in line:
                return_dict["OS Type"] = "ios"
                break
            elif "IOS-XR" in line:
                return_dict["OS Type"] = "iosxr"
                break
            elif "Cisco Nexus" in line:
                return_dict["OS Type"] = "nxos_ssh"
                break
            elif "IOSv" in line:
                return_dict["OS Type"] = "ios"
                break
        return return_dict
    elif header == "Linux":
        stdin_lines, stdout_lines, stderr_lines = ssh_open.exec_command("uname -a")
        if stderr_lines.readlines():
            raise ValueError(f"Something happened when connecting to {address}")
        stdout_list = stdout_lines.readlines()
        return_dict = {"Version Info": [stdout_list[0].strip()]}
        if "Ubuntu" in return_dict["Version Info"]:
            return_dict["OS Type"] = "Ubuntu"
        else:
            return_dict["OS Type"] = "Linux"
        return return_dict
    elif header == "Other":
        stdin_lines, stdout_lines, stderr_lines = ssh_open.exec_command("show version")
        # print(stdout_lines.readlines())
        # print(stderr_lines.readlines())
    ssh_open.close()


def get_config_napalm(
    dev_driver=None,
    host=None,
    port=None,
    usern=None,
    passw=None,
    enable_password=None,
):
    """
    Will use napalm to connect to the device.  It will return a dictionary of the configs cleaned with no new lines, etc
    If full_config is True, it returns the full config
    get_config_napalm(dev_driver=device_type["OS Type"], host=address, usern=username, passw=password)
    Args:
        dev_driver (str) : device driver to use with napalm for connecting
        host (str) : ip address of the device connecting to
        port (int) :  port connecting to so can pass if not regular SSH
        usern (str) : username to use to connect to the device
        passw (str) : password to use to connect to the device
        enable_password (str|None) : enable_password will be None if no enable password is needed else it will be a string of the enable password
    """
    for item in [dev_driver, host, usern, passw]:
        if not isinstance(item, str):
            raise TypeError(f"{item} is not a string.  It is a {type(item).__name__}")
    if not isinstance(port, int):
        raise TypeError(f"{port} is not an int.  It is a {type(port).__name__}")
    try:
        ipaddress.IPv4Address(host)
    except ipaddress.AddressValueError:
        raise ipaddress.AddressValueError(
            f"{host} is not set up to be an IPv4 adddress."
        )
    if enable_password is not None and not isinstance(enable_password, str):
        raise TypeError(
            f"{enable_password} is not a string.  It is a {type(port).__name__}"
        )

    if dev_driver not in [
        "eos",
        "junos",
        "iosxr",
        "nxos",
        "nxos_ssh",
        "ios",
    ]:
        raise ValueError(f"{dev_driver} is not an approved device driver")
    if port < 0 or port > 65535:
        raise ValueError(f"Port number needs to be between 0 and 65535")
    device_driver = napalm.get_network_driver(dev_driver)
    optional_args = None
    if dev_driver == "ios" or dev_driver == "nxos_ssh":
        if enable_password is not None:
            if optional_args is None:
                optional_args = {}
            optional_args["secret"] = enable_password
    with device_driver(host, usern, passw, optional_args=optional_args) as device:
        print("Attempting to get the device configuration...")
        try:
            device_facts = device.get_facts()
        except NotImplementedError:
            device_facts = {"Not_Implemented": "Not_Implemented"}
        try:
            device_config = device.get_config()
        except NotImplementedError:
            device_config = {"Not_Implemented": "Not_Implemented"}
        try:
            device_config_full = device.get_config(full=True)
        except NotImplementedError:
            device_config_full = {"Not_Implemented": "Not_Implemented"}
        try:
            device_optics = device.get_optics()
        except NotImplementedError:
            device_optics = {"Not_Implemented": "Not_Implemented"}
        try:
            device_network_instances = device.get_network_instances()
        except NotImplementedError:
            device_network_instances = {"Not_Implemented": "Not_Implemented"}
        try:
            device_lldp_detail = device.get_lldp_neighbors_detail()
        except NotImplementedError:
            device_lldp_detail = {"Not_Implemented": "Not_Implemented"}
        try:
            device_lldp = device.get_lldp_neighbors()
        except NotImplementedError:
            device_lldp = {"Not_Implemented": "Not_Implemented"}
        try:
            device_environment = device.get_environment()
        except NotImplementedError:
            device_environment = {"Not_Implemented": "Not_Implemented"}
        try:
            device_interfaces = device.get_interfaces()
        except NotImplementedError:
            device_interfaces = {"Not_Implemented": "Not_Implemented"}
        try:
            device_interfaces_ip = device.get_interfaces_ip()
        except NotImplementedError:
            device_interfaces_ip = {"Not_Implemented": "Not_Implemented"}
        try:
            device_snmp_info = device.get_snmp_information()
        except NotImplementedError:
            device_snmp_info = {"Not_Implemented": "Not_Implemented"}
        try:
            device_users = device.get_users()
        except NotImplementedError:
            device_users = {"Not_Implemented": "Not_Implemented"}
    return_dict = {}
    return_dict["Device_Facts"] = device_facts
    return_dict["Device_Optics"] = device_optics
    return_dict["Device_Network_Instances"] = device_network_instances
    return_dict["Device_LLDP_Detail"] = device_lldp_detail
    return_dict["Device_LLDP"] = device_lldp
    return_dict["Device_Environment"] = device_environment
    return_dict["Device_Interfaces"] = device_interfaces
    return_dict["Device_Interfaces_IP"] = device_interfaces_ip
    return_dict["Device_SNMP_Information"] = device_snmp_info
    return_dict["Device_Users"] = device_users
    write_directory = directory_checker(host)
    config_dict = {
        "startup": "Device_Startup_Config",
        "running": "Device_Running_Config",
        "candidate": "Device_Candidate_Config",
    }
    for key, value in config_dict.items():
        file_location = f"{write_directory}\\{host}_{key}.txt"
        with open(file_location, "w") as output:
            output.write(device_config[key])
        return_dict[f"{value}_File_Location"] = file_location
    for key, value in config_dict.items():
        file_location = f"{write_directory}\\{host}_{key}_full.txt"
        with open(file_location, "w") as output:
            output.write(device_config_full[key])
        return_dict[f"{value}_Full_File_Location"] = file_location
    return return_dict


def directory_checker(address):
    """
    Uses the address of the device to create a directory for storing configs.
    First sees if the directory exists and then creates it if need be
    Args:
        address (str) : IP of the device connecting to for which configs will be stored
    Return
        str : directory path that will be written to
    """
    if address is None:
        raise ValueError(f"{address} needs to be a string and not None")
    if not isinstance(address, str):
        raise ValueError(f"{address} needs to be a string and not None")
    write_directory = f"{parentdir}\\Output\\Scans\\{address}"
    if not os.path.exists(write_directory):
        os.makedirs(write_directory)
    return write_directory


def device_grab(
    address=None,
    port_dict=None,
    username=None,
    password=None,
    enable_password_needed=False,
    enable_password=None,
):
    """
    This will do a bunch of things.  The main one is iterate through the ports the user passes over
    and see if single port, list of ports, or dictionary of ports.
    It will then connect to the machine at address and see if it can SSH to the device.  Once there it will attempt to determine version of the
    device if Cisco.  If LInux, it will grab the uname information only.
    If config is gotten, it can be written to a file to as well
    Args:
        address (ipaddress.IPv4Address or string) : IPv4 address of ipaddress.IPv4Address type that will be used to connect to
        port_dict (dict) : dictionary of either one port or multiple ports of format {<port_number>:<header>}
        username (str) : string of the username.  If not given, user will be asked
        password (str) : strin of the password.  If not given, user will be asked
        enable_password_needed (bool) : if True, enable password needs to either be passed or will be asked for.  If False, enable password check is skipped and password set to None
        enable_password (str) : string of the enable password.  If not given, user will be asked

    Return:
        dictionary of dictionaries : dictionary will contain full and not full config and full and not full will contain start, run, and candidate
    """
    connect_address = check_address(address)
    ssh_port, ssh_open = check_ports(port_dict)
    return_dict = {}
    return_dict = {
        "Version_Info": ["No Version information was available"],
        "CONFIG": {
            "Open_Close": False,
            "Open_Close_Msg": "SSH is not open on the device for ports scanned",
            "Device_Information": {},
        },
    }
    if ssh_port is False and ssh_open is False:
        return_dict["CONFIG"] = {
            "Open_Close": False,
            "Open_Close_Msg": "SSH is not open on the device for ports scanned",
            "Device_Information": {},
        }
        return return_dict
    ssh_username = check_username(username, connect_address)
    ssh_password = check_password(password, connect_address)
    if enable_password_needed is True:
        ssh_enable_password = check_enable_password(enable_password, connect_address)
    elif enable_password_needed is False:
        ssh_enable_password = None
    else:
        raise ValueError(
            f"You set the enable_password_needed option to something besides True or False.  Not Cool man.  enable_password_needed = {enable_password_needed}"
        )
    device_type = get_device_type(
        connect_address,
        ssh_port,
        ssh_username,
        ssh_password,
        ssh_enable_password,
        ssh_open,
    )
    if "[ERROR] " in device_type["Version Info"]:
        return_dict = {
            "Version_Info": device_type["Version Info"],
        }
        return return_dict
    return_dict = {
        "Version_Info": device_type["Version Info"],
        "CONFIG": {
            "Open_Close": False,
            "Open_Close_Msg": f"Config for type device not yet supported ({device_type['OS Type']}).",
            "Device_Information": {},
        },
    }
    if device_type["OS Type"] in [
        "eos",
        "junos",
        "iosxr",
        "nxos",
        "nxos_ssh",
        "ios",
    ]:
        return_dict = {
            "Version_Info": device_type["Version Info"],
            "CONFIG": {
                "Open_Close": True,
                "Open_Close_Msg": f"SSH is open and Device Type is known ({device_type['OS Type']}).",
            },
        }
        device_information = get_config_napalm(
            dev_driver=device_type["OS Type"],
            host=connect_address,
            port=ssh_port,
            usern=ssh_username,
            passw=ssh_password,
            enable_password=ssh_enable_password,
        )
        return_dict["CONFIG"]["Device_Information"] = device_information
    return return_dict


if __name__ == "__main__":
    start_time = time.time()
    linux_testbox = ipaddress.ip_address("192.168.89.80")
    cisco_iosxe_no_en = ipaddress.ip_address("192.168.89.254")
    cisco_iosv_enable = ipaddress.ip_address("192.168.89.253")
    cisco_iosl2_no_enable = ipaddress.ip_address("192.168.89.252")
    cisco_nx0s7 = ipaddress.ip_address("192.168.89.251")
    cisco_iosxe_enable = ipaddress.ip_address("192.168.89.247")
    fake_testbox = ipaddress.ip_address("192.168.1.65")
    response_time = (1.1, 1.35, 1.82)
    linux_ports = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
        }
    }
    cisco_ports = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-1.99-Cisco-1.25"},
        }
    }
    fake_ports = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
        }
    }
    linux_test_device = FoundDevice(linux_testbox, response_time)
    cisco_iosxe_no_en_device = FoundDevice(cisco_iosxe_no_en, response_time)
    cisco_iosv_enable_device = FoundDevice(cisco_iosv_enable, response_time)
    cisco_iosl2_no_enable_device = FoundDevice(cisco_iosl2_no_enable, response_time)
    cisco_nx0s7_device = FoundDevice(cisco_nx0s7, response_time)
    cisco_iosxe_enable_device = FoundDevice(cisco_iosxe_enable, response_time)
    fake_testbox_device = FoundDevice(fake_testbox, response_time)

    linux_test_device.all_ports = linux_ports
    cisco_iosxe_no_en_device.all_ports = cisco_ports
    cisco_iosv_enable_device.all_ports = cisco_ports
    cisco_iosl2_no_enable_device.all_ports = cisco_ports
    cisco_nx0s7_device.all_ports = cisco_ports
    cisco_iosxe_enable_device.all_ports = cisco_ports
    fake_testbox_device.all_ports = fake_ports

    username = "jmctsm"
    password = "WWTwwt1!"
    enable_password = None
    no_enable_device_list = [
        fake_testbox_device,
        linux_test_device,
        cisco_iosxe_no_en_device,
        cisco_iosl2_no_enable_device,
        cisco_nx0s7_device,
    ]
    enable_device_list = [
        cisco_iosv_enable_device,
        cisco_iosxe_enable_device,
    ]
    json_input_dict = {}
    for device in no_enable_device_list:
        device_grab_info = device_grab(
            address=device.IP,
            port_dict=device.open_tcp_ports,
            username=username,
            password=password,
            enable_password_needed=False,
        )
        json_input_dict[str(device.IP)] = device_grab_info

    enable_password = "WWTwwt1!"

    for device in enable_device_list:
        device_grab_info = device_grab(
            address=device.IP,
            port_dict=device.open_tcp_ports,
            username=username,
            password=password,
            enable_password_needed=True,
            enable_password=enable_password,
        )
        json_input_dict[str(device.IP)] = device_grab_info

    print(json_input_dict)
    json_output = json.dumps(json_input_dict, indent=4)
    print("\n\n\n\n")
    print(json_output)
    with open(f"Output\\test_output_{time.time()}.txt", "w") as file_output:
        file_output.write(json_output)
    duration = time.time() - start_time
    print(f"Duration to run was {duration}")