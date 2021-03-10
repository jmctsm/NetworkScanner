#!python

"""
This will connect to a device that is Cisco and attempt to get the config from that device
"""

from device_class import FoundDevice
import ipaddress
import time


def grab_config(
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
    pass


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
    device_list = [fake_test_device, linux_test_device, cisco_test_device]
    for device in device_list:
        grab_config(address=device.IP, port_dict=device.open_tcp_ports)
