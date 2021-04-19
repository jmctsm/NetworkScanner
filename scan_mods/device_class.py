#!python

"""
    This is a class for the devices that are being scanned in the NetworkScanner application
"""

import ipaddress
import os
import re
import time
import json
import sys

# sys.path.append("../")


if "scan_mods" in os.listdir(os.getcwd()):
    sys.path.append(os.getcwd())

else:
    path = "../"
    while True:
        if "scan_mods" in os.listdir(path):
            sys.path.append(path)
            break
        else:
            path += "../"

from scan_mods.grabbing_mods.device_grabber import device_grab
from scan_mods.mp_port_scanner import port_scanner


class FoundDevice:
    """
    Class to define the devices being scanned

    Attributes:
        ._IP = string that can be an IPaddress object
        ._response_time = response time tuple from pinger
        ._ports = dict of open ports and headers

    Methods:
        .__init__() : initializes the class using the return time from ping and the IP of the device.  Sets the other attributes to blanks
        .open_ports() : property to set and get ._open_ports attribute
        .response_time() : property method to get ._response_time attribute
        .IP() : property method to get .IP attribute
    """

    def __init__(
        self,
        address,
        time_tuple,
        username=None,
        password=None,
        use_enable=False,
        enable_password=None,
        domain_name=None,
    ):
        if not isinstance(address, str):
            raise TypeError("address it not of valid type string.  Please try again.")
        try:
            ipaddress.ip_address(address)
        except ValueError:
            raise ValueError(f"{address} is not a valid IP address.  Please try again.")
        if not isinstance(time_tuple, tuple):
            raise TypeError(f"{time_tuple} is not an instance of tuple")
        if len(time_tuple) != 3:
            raise ValueError(
                f"The length of the response times should be 3.  You submitted {time_tuple}"
            )
        for time in time_tuple:
            if not isinstance(time, float):
                raise TypeError(f"The tuple is not a tuple of length 3 floats")
        self._IP = address
        self._response_time = time_tuple
        self._all_ports = None
        self._open_tcp_ports = {}
        self._open_udp_ports = {}
        self._closed_tcp_ports = {}
        self._closed_udp_ports = {}
        self._username = username
        self._password = password
        self._use_enable = use_enable
        self._enable_password = enable_password
        self._domain_name = domain_name
        self.device_info = None

    @property
    def IP(self) -> str:
        return self._IP

    @property
    def response_time(self) -> tuple:
        return self._response_time

    @property
    def username(self):
        if self._username is None:
            return "Username has not been set yet"
        return self._username

    @property
    def password(self):
        if self._password is None:
            return "Password for device has not been given"
        return "Password for device has been given"

    @property
    def enable_password(self):
        if self._use_enable:
            if self._enable_password is None:
                return "Enable password for device has not been given"
            return "Enable password for device has been given"
        return "Not using Enable password for this device"

    @property
    def domain_name(self):
        if self._domain_name is None:
            return "Domain name has not been set yet"
        return self._domain_name

    def get_ports(self):
        self.all_ports = port_scanner(self.IP, self.domain_name)

    @property
    def all_ports(self):
        """
        returns the _all_ports attribute.  If None, return False
        """
        if self._all_ports is None:
            return None
        return self._all_ports

    @all_ports.setter
    def all_ports(self, ports_headers):
        """
        all_ports setter to set the all ports section
        ONce the ports are set, the ports are split as well into tcp open and closed
            as well as UDP open and closed
        Args:
            ports_headers (dict) : key is either TCP<Port_number> or UDP_<Port_Number> and value is the header or error message
        """
        if isinstance(ports_headers, dict):
            if self._all_ports is None:
                self._all_ports = {"TCP": {}, "UDP": {}}
                for key in ports_headers.keys():
                    if key == "TCP" or key == "UDP":
                        if isinstance(ports_headers[key], dict):
                            self._all_ports[key] = ports_headers[key]
                        else:
                            raise TypeError(
                                f"{ports_headers[key]} is not a dictionary.  "
                                f"It was {type(ports_headers[key]).__name__}"
                            )
                    else:
                        raise KeyError(
                            f"{key} does not follow standard of 'TCP' or 'UDP'"
                        )
            else:
                for key in ports_headers.keys():
                    if key == "TCP" or key == "UDP":
                        if isinstance(ports_headers[key], dict):
                            for port_key in ports_headers[key].keys():
                                if isinstance(ports_headers[key][port_key], dict):
                                    self._all_ports[key][port_key] = ports_headers[key][
                                        port_key
                                    ]
                                else:
                                    raise TypeError(
                                        f"{ports_headers[key]} is not a dictionary.  "
                                        f"It was {type(ports_headers[key]).__name__}"
                                    )
                        else:
                            raise TypeError(
                                f"{ports_headers[key]} is not a dictionary.  "
                                f"It was {type(ports_headers[key]).__name__}"
                            )
                    else:
                        raise KeyError(
                            f"{key} does not follow standard of 'TCP' or 'UDP'"
                        )
        else:
            raise TypeError(
                f"ports variable passed in was not a dictionary.  It was {type(ports_headers).__name__}."
                f"  You may want to fix that."
            )

        for protocol_key in self._all_ports.keys():
            if protocol_key == "TCP":
                for port_key in self._all_ports["TCP"].keys():
                    if isinstance(self._all_ports["TCP"][port_key], dict):
                        if (
                            len(list(self._all_ports["TCP"][port_key].keys())) == 1
                            and list(self._all_ports["TCP"][port_key].keys())[0]
                            == "ERROR"
                        ):
                            self._closed_tcp_ports[port_key] = self._all_ports["TCP"][
                                port_key
                            ]
                        else:
                            self._open_tcp_ports[port_key] = self._all_ports["TCP"][
                                port_key
                            ]
                    else:
                        raise TypeError(f"{type(port_key).__name__} is not a dict.")
            if protocol_key == "UDP":
                for port_key in self._all_ports["UDP"].keys():
                    if isinstance(self._all_ports["UDP"][port_key], dict):
                        if (
                            len(list(self._all_ports["UDP"][port_key].keys())) == 1
                            and list(self._all_ports["UDP"][port_key].keys())[0]
                            == "ERROR"
                        ):
                            self._closed_udp_ports[port_key] = self._all_ports["UDP"][
                                port_key
                            ]
                        else:
                            self._open_udp_ports[port_key] = self._all_ports["UDP"][
                                port_key
                            ]
                    else:
                        raise TypeError(f"{type(port_key).__name__} is not a dict.")
        try:
            assert len(self._all_ports["TCP"]) == len(self._open_tcp_ports) + len(
                self._closed_tcp_ports
            )
        except AssertionError:
            raise AssertionError(
                f"The length of the ports categorized does not equal the length of the number of ports for TCP"
            )
        try:
            assert len(self._all_ports["UDP"]) == len(self._open_udp_ports) + len(
                self._closed_udp_ports
            )
        except AssertionError:
            raise AssertionError(
                f"The length of the ports categorized does not equal the length of the number of ports for UDP"
            )

    @property
    def open_tcp_ports(self):
        """
        Getter for the open TCP ports for the device
        Return:
            dict : dictionary of the open ports in port_number: header
        """
        return self._open_tcp_ports

    @property
    def open_udp_ports(self):
        """
        Getter for the open UDP ports for the device
        Return:
            dict : dictionary of the open ports in port_number: header
        """
        return self._open_udp_ports

    @property
    def closed_tcp_ports(self):
        """
        Getter for the closed TCP ports for the device
        Return:
            dict : dictionary of the closed ports in port_number: header
        """
        return self._closed_tcp_ports

    @property
    def closed_udp_ports(self):
        """
        Getter for the closed UDP ports for the device
        Return:
            dict : dictionary of the closed ports in port_number: header
        """
        return self._closed_udp_ports

    def __hash__(self) -> int:
        return hash(self.IP)

    def __bool__(self) -> bool:
        return bool(self.IP)

    def __eq__(self, other: object) -> bool:
        """
        Basically if the IPs are equal then the class is equal to whatever is being tested
        """
        if isinstance(other, str):
            try:
                ipaddress.ip_address(other)
            except ValueError:
                return False
            if other == self.IP:
                return True
            return False
        if isinstance(other, FoundDevice):
            if other.IP == self.IP:
                return True
            return False
        if isinstance(other, ipaddress.IPv4Address):
            if str(other) == self.IP:
                return True
            return False
        return False

    def device_info_grabber(self):
        """
        This will use the scan_mods.device_grabber to get the information from each device and return it in a JSON format
        """
        self.device_info = device_grab(
            address=self.IP,
            port_dict=self.open_tcp_ports,
            username=self._username,
            password=self._password,
            enable_password_needed=self._use_enable,
            enable_password=self._enable_password,
        )

    def __repr__(self) -> str:
        # This needs to be expanded and the test updated for it too
        return_string = f"{self.IP} : "
        return_string += f"\n\tresponse times are {self.response_time[0]} ms, {self.response_time[1]} ms, {self.response_time[2]} ms"
        return_string += f"\n\tusername is {self.username}"
        return_string += f"\n\tpassword {self.password}"
        return_string += f"\n\tenable password {self.enable_password}"
        return_string += f"\n\tdomain name is {self.domain_name}"
        if self.all_ports is not None:
            return_string += "\n\tOpen TCP Ports:"
            for key in self.open_tcp_ports.keys():
                return_string += f"\n\t\t{key} : {self.open_tcp_ports[key]}"
            return_string += "\n\tOpen UDP Ports:"
            for key in self.open_udp_ports.keys():
                return_string += f"\n\t\t{key} : {self.open_udp_ports[key]}"
            return_string += "\n\tClosed TCP Ports:"
            for key in self.closed_tcp_ports.keys():
                return_string += f"\n\t\t{key} : {self.closed_tcp_ports[key]}"
            return_string += "\n\tClosed UDP Ports:"
            for key in self.closed_udp_ports.keys():
                return_string += f"\n\t\t{key} : {self.closed_udp_ports[key]}"
        return return_string

    def __str__(self) -> str:
        # This needs to be expanded and the test updated for it too
        return_string = f"{self.IP} : "
        return_string += f"\n\tresponse times are {self.response_time[0]} ms, {self.response_time[1]} ms, {self.response_time[2]} ms"
        return_string += f"\n\tusername is {self.username}"
        return_string += f"\n\tpassword {self.password}"
        return_string += f"\n\tenable password {self.enable_password}"
        return_string += f"\n\tdomain name is {self.domain_name}"
        if self.all_ports is not None:
            return_string += "\n\tOpen TCP Ports:"
            for key in self.open_tcp_ports.keys():
                return_string += f"\n\t\t{key} = {self.open_tcp_ports[key]}"
            return_string += "\n\tOpen UDP Ports:"
            for key in self.open_udp_ports.keys():
                return_string += f"\n\t\t{key} = {self.open_udp_ports[key]}"
            return_string += "\n\tClosed TCP Ports:"
            for key in self.closed_tcp_ports.keys():
                return_string += f"\n\t\t{key}"
            return_string += "\n\tClosed UDP Ports:"
            for key in self.closed_udp_ports.keys():
                return_string += f"\n\t\t{key}"
        return return_string

    def print_json_short(self):
        """
        Will take the class and make a JSON representation of it that is only port numbers
        ARgs:
            none
        Return:
            JSON string for printing or output to a file
        """
        output = {}
        output[str(self.IP)] = {
            "ping_response_times": self.response_time,
            "username": self.username,
            "password": self.password,
            "enable_password": self.enable_password,
            "domain_name": self.domain_name,
        }
        if self.all_ports is not None:
            output[str(self.IP)]["Open_TCP_Ports_List"] = list(
                self.open_tcp_ports.keys()
            )
            output[str(self.IP)]["Open_UDP_Ports_List"] = list(
                self.open_udp_ports.keys()
            )
            output[str(self.IP)]["Closed_TCP_Ports_List"] = list(
                self.closed_tcp_ports.keys()
            )
            output[str(self.IP)]["Closed_UDP_Ports_List"] = list(
                self.closed_udp_ports.keys()
            )
        if self.device_info is not None:
            output[self.IP]["Device_Info"] = self.device_info["Version_Info"]
        return json.dumps(output, indent=4)

    def print_json_long(self):
        """
        Will take the class and make a JSON representation of it with port numbers and headers
        ARgs:
            none
        Return:
            JSON string for printing or output to a file
        """
        output = {}
        output[str(self.IP)] = {
            "ping_response_times": self.response_time,
            "username": self.username,
            "password": self.password,
            "enable_password": self.enable_password,
            "domain_name": self.domain_name,
        }
        if self.all_ports is not None:
            output[str(self.IP)]["Open_TCP_Ports_List"] = self.open_tcp_ports
            output[str(self.IP)]["Open_UDP_Ports_List"] = self.open_udp_ports
            output[str(self.IP)]["Closed_TCP_Ports_List"] = self.closed_tcp_ports
            output[str(self.IP)]["Closed_UDP_Ports_List"] = self.closed_udp_ports
        if self.device_info is not None:
            output[self.IP]["Device_Info"] = self.device_info
        return json.dumps(output, indent=4)


if __name__ == "__main__":
    start_time = time.time()
    address01 = "192.168.89.80"
    address02 = "192.168.89.254"
    address03 = "192.168.89.253"
    address04 = "192.168.89.252"
    address05 = "192.168.89.251"
    address06 = "192.168.89.247"
    address07 = "192.168.0.254"

    response_time01 = (1.1, 1.35, 1.82)
    response_time02 = (1.2, 1.35, 1.82)
    response_time03 = (1.3, 1.35, 1.82)
    response_time04 = (1.4, 1.35, 1.82)
    response_time05 = (1.5, 1.35, 1.82)
    response_time06 = (1.6, 1.35, 1.82)
    response_time07 = (1.7, 1.35, 1.82)

    domain_name = "test.local"
    username = "jmctsm"
    password = "ciscocisco"
    enable_password = "ciscocisco"

    device_list = []
    device_list.append(
        FoundDevice(
            address01,
            response_time01,
            username=username,
            password=password,
            domain_name=domain_name,
        )
    )
    device_list.append(
        FoundDevice(
            address02,
            response_time02,
            username=username,
            password=password,
            domain_name=domain_name,
        )
    )
    device_list.append(
        FoundDevice(
            address03,
            response_time03,
            username=username,
            password=password,
            domain_name=domain_name,
            use_enable=True,
            enable_password=enable_password,
        )
    )
    device_list.append(
        FoundDevice(
            address04,
            response_time04,
            username=username,
            password=password,
            domain_name=domain_name,
        )
    )
    device_list.append(
        FoundDevice(
            address05,
            response_time05,
            username=username,
            password=password,
            domain_name=domain_name,
        )
    )
    device_list.append(
        FoundDevice(
            address06,
            response_time06,
            username=username,
            password=password,
            domain_name=domain_name,
            use_enable=True,
            enable_password=enable_password,
        )
    )
    device_list.append(
        FoundDevice(
            address07,
            response_time07,
            username=username,
            password=password,
            domain_name=domain_name,
        )
    )

    for device in device_list:
        print(device.IP)
        device.get_ports()

    for device in device_list:
        print(device.IP)
        device.device_info_grabber()

    for device in device_list:
        print(repr(device))

    print("\n\n\n\n")

    for device in device_list:
        print(device)

    print("\n\n\n\n")

    for device in device_list:
        print(device.print_json_short())
        write_directory = None
        if "Output" in os.listdir(os.getcwd()):
            write_directory = f"{os.getcwd()}/Output/Scans/{device.IP}"
        else:
            path = "../"
            while write_directory is None:
                if "Output" in os.listdir(path):
                    write_directory = f"{path}/Output/Scans/{device.IP}"
                path += "../"
        if not os.path.exists(write_directory):
            os.makedirs(write_directory)
        file_location = f"{write_directory}\\{device.IP}_json_short.txt"
        with open(file_location, "w") as output_file:
            output_file.write(device.print_json_short())

    print("\n\n\n\n")

    for device in device_list:
        print(device.print_json_long())
        write_directory = None
        if "Output" in os.listdir(os.getcwd()):
            write_directory = f"{os.getcwd()}/Output/Scans/{device.IP}"
        else:
            path = "../"
            while write_directory is None:
                if "Output" in os.listdir(path):
                    write_directory = f"{path}/Output/Scans/{device.IP}"
                path += "../"
        if not os.path.exists(write_directory):
            os.makedirs(write_directory)
        file_location = f"{write_directory}\\{device.IP}_json_long.txt"
        with open(file_location, "w") as output_file:
            output_file.write(device.print_json_long())

    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")