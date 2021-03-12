#!python

"""
This will connect to a device that is Cisco and attempt to get the config from that device
"""

from typing import Type
from device_class import FoundDevice
import ipaddress
import time
import getpass
import napalm
import paramiko
import json


def check_address(address):
    """
    Checks to see if the address is a string or a ipaddress.IPv4Address type
    Checks to make sure that it is valid
    If all good, returns an address string
    If bad, raises exception
    Args:
        address (ipaddress.IPv4Address or string) : IPv4 address of ipaddress.IPv4Address type that will be used to connect to
    return:
        string : address string
    """
    if address is None:
        raise ValueError(f"No address was given.  Please don't do that again.")
    if isinstance(address, str):
        try:
            ipaddress.IPv4Address(address)
        except ipaddress.AddressValueError:
            raise ipaddress.AddressValueError(
                f"{address} is not set up to be an IPv4 adddress."
            )
        else:
            return address
    if isinstance(address, ipaddress.IPv4Address):
        return str(address)
    raise TypeError(f"{address} is not a viable address type")


def check_ports(port_dictionary):
    """
    This will run through the ports that are supposedly open and see if 22 is listed.  If so, it will return the device type if it can be determined
    or False if not open
    Args:
        port_dictionary (dict) : dictionary of either one port or multiple ports of format {<port_number>:<header>}
    Return
        False : if 22 is not in the list
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
            for value in port_dictionary[key].values():
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


def check_username(name, address):
    """
    This will check to see if a username is given or if one needs to be asked for
    Args:
        name (None|str) : this will be None if no username is given or check to make sure a string otherwise.
        address (str) : string of the address getting username for
    return:
        str : username either validated or gotten from a user
    """
    while True:
        if name is None or not isinstance(name, str):
            name = input(f"Please enter your username for system at IP {address}: ")
        if name is not None and isinstance(name, str):
            if len(name) < 255:
                if len(name) > 0:
                    return name
                else:
                    print(
                        f"Username was less than 1 character.  Please re-enter the CORRECT username"
                    )
            else:
                print(
                    f"Username was greater than 255 characters.  Why the heck did you do that?"
                )
            name = None


def check_password(password, address):
    """
    This will check to see if a password is given or if one needs to be asked for
    Args:
        password (None|str) : this will be None if no password is given or check to make sure a string otherwise.
        address (str) : string of the address getting password for
    return:
        str : password either validated or gotten from a user
    """
    while True:
        if password is None or not isinstance(password, str):
            password = getpass.getpass(
                f"Please enter your password for system at IP {address}: "
            )
        if password is not None and isinstance(password, str):
            if len(password) > 0:
                return password
            else:
                print(
                    f"Username was less than 1 character.  Please re-enter the CORRECT username"
                )
            password = None


def get_device_type(address, port, username, password, header):
    """
    Will attempt to connect to a device and determine the device type for napalm
    Args:
        address (str) : string of the IP to connect to
        port (int) : integer of the port connecting to
        username (str): string of the username
        password (str): string of the password
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

    ssh_open = paramiko.SSHClient()
    ssh_open.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Attempting connection to {address}")
    try:
        # to work for Cisco added in the look_for_keys and allow_agent parameters
        ssh_open.connect(
            address, port, username, password, look_for_keys=False, allow_agent=False
        )
    except paramiko.AuthenticationException:
        raise paramiko.AuthenticationException(
            f"Authentication failed for device {address}"
        )
    if header == "Cisco":
        stdin_lines, stdout_lines, stderr_lines = ssh_open.exec_command("show version")
        if stderr_lines.readlines():
            raise ValueError(f"Something happened when connecting to {address}")
        # print(stdout_lines.readlines())
        # stdout_list = stdout_lines.readlines()
        stdout_list = []
        for line in stdout_lines.readlines():
            if line.strip() == "":
                continue
            stdout_list.append(line.strip())
        return_dict = {"Version Info": stdout_list}
        for line in stdout_list:
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
        return return_dict
    elif header == "Linux":
        stdin_lines, stdout_lines, stderr_lines = ssh_open.exec_command("uname -a")
        if stderr_lines.readlines():
            raise ValueError(f"Something happened when connecting to {address}")
        stdout_list = stdout_lines.readlines()
        return_dict = {"Version Info": stdout_list[0].strip()}
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
    dev_driver=None, host=None, port=None, usern=None, passw=None, full_config=False
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
        full_config (bool) : True means get the full config for all.  False is just the regular config
    """
    for item in [dev_driver, host, usern, passw]:
        if not isinstance(item, str):
            raise TypeError(f"{item} is not a string.  It is a {type(item).__name__}")
    if not isinstance(port, int):
        raise TypeError(f"{port} is not an int.  It is a {type(port).__name__}")
    if not isinstance(full_config, bool):
        raise TypeError(
            f"{full_config} is not a boolean.  It is a {type(full_config).__name__}"
        )
    try:
        ipaddress.IPv4Address(host)
    except ipaddress.AddressValueError:
        raise ipaddress.AddressValueError(
            f"{host} is not set up to be an IPv4 adddress."
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
    # driver = get_network_driver('eos')
    # optional_args = {'my_optional_arg1': 'my_value1', 'my_optional_arg2': 'my_value2'}
    # device = driver('192.168.76.10', 'dbarroso', 'this_is_not_a_secure_password', optional_args=optional_args)
    # device.open()
    device_driver = napalm.get_network_driver(dev_driver)
    with device_driver(host, usern, passw) as device:
        device_facts = device.get_facts()
        device_startup_config = device.get_config()
        device_startup_config_full = device.get_config(full=True)
        device_optics = device.get_optics()
        device_network_instances = device.get_network_instances()
        device_lldp_detail = device.get_lldp_neighbors_detail()
        device_lldp = device.get_lldp_neighbors()
        device_environment = device.get_environment()
    return_dict = {}
    return_dict["Device_Facts"] = device_facts
    return_dict["Device_Startup_Config"] = device_startup_config["startup"]
    return_dict["Device_Running_Config"] = device_startup_config["running"]
    return_dict["Device_Candidate_Config"] = device_startup_config["candidate"]
    # return_dict["Device_Startup_Config_Full"] = device_startup_config_full["startup"]
    # return_dict["Device_Running_Config_Full"] = device_startup_config_full["running"]
    return_dict["Device_Candidate_Config_Full"] = device_startup_config_full[
        "candidate"
    ]
    return_dict["Device_Optics"] = device_optics
    return_dict["Device_Network_Instances"] = device_network_instances
    return_dict["Device_LLDP_Detail"] = device_lldp_detail
    return_dict["Device_LLDP"] = device_lldp
    return_dict["Device_Environment"] = device_environment
    return return_dict


def device_grab(
    address=None,
    port_dict=None,
    username=None,
    password=None,
    write_config=False,
    output_directory=None,
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
        write_config (bool) : if True, all configs are written to specific files
        output_directory (str) : output directory base for files to be written to.  If None, uses local file location

    Return:
        dictionary of dictionaries : dictionary will contain full and not full config and full and not full will contain start, run, and candidate
    """
    connect_address = check_address(address)
    ssh_port, ssh_open = check_ports(port_dict)
    if ssh_port is False and ssh_open is False:
        return_dict = {
            "CONFIG": {
                "Open_Close": False,
                "Open_Close_Msg": "SSH is not open on the device for ports scanned",
                "Device_Information": {},
            }
        }
        return return_dict
    ssh_username = check_username(username, connect_address)
    ssh_password = check_password(password, connect_address)
    device_type = get_device_type(
        connect_address, ssh_port, ssh_username, ssh_password, ssh_open
    )
    return_dict = {
        "CONFIG": {
            "Open_Close": False,
            "Open_Close_Msg": f"Config for type device not yet supported ({device_type['OS Type']}).",
            "Device_Information": {},
        }
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
            "CONFIG": {
                "Open_Close": True,
                "Open_Close_Msg": f"SSH is open and Device Type is known ({device_type['OS Type']}).",
            }
        }
        device_information = get_config_napalm(
            dev_driver=device_type["OS Type"],
            host=connect_address,
            port=ssh_port,
            usern=ssh_username,
            passw=ssh_password,
            full_config=False,
        )
        return_dict["CONFIG"]["Device_Information"] = device_information

    if write_config:
        # will create a function that tests output dir and then writes the configs to this directory
        # output_directory
        pass
    return return_dict


if __name__ == "__main__":
    start_time = time.time()
    linux_testbox = ipaddress.ip_address("192.168.89.80")
    cisco_testbox = ipaddress.ip_address("192.168.89.22")
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
    cisco_test_device = FoundDevice(cisco_testbox, response_time)
    fake_test_device = FoundDevice(fake_testbox, response_time)
    linux_test_device.all_ports = linux_ports
    cisco_test_device.all_ports = cisco_ports
    fake_test_device.all_ports = fake_ports
    username = "jmctsm"
    password = "WWTwwt1!"
    device_list = [fake_test_device, linux_test_device, cisco_test_device]
    json_input_dict = {}
    for device in device_list:
        device_grab_info = device_grab(
            address=device.IP,
            port_dict=device.open_tcp_ports,
            username=username,
            password=password,
        )
        json_input_dict[str(device.IP)] = device_grab_info
    print(json_input_dict)
    json_output = json.dumps(json_input_dict)
    print("\n\n\n\n")
    print(json_output)
