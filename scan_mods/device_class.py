#!python

"""
    This is a class for the devices that are being scanned in the NetworkScanner application
"""

import ipaddress
import os
import re
import time
import json


class FoundDevice:
    """
    Class to define the devices being scanned

    Attributes:
        ._IP = IPv4 object for the IP being scanned
        ._response_time = response time tuple from pinger
        ._ports = dict of open ports and headers

    Methods:
        .__init__() : initializes the class using the return time from ping and the IP of the device.  Sets the other attributes to blanks
        .open_ports() : property to set and get ._open_ports attribute
        .response_time() : property method to get ._response_time attribute
        .IP() : property method to get .IP attribute
    """

    def __init__(self, address, time_tuple):
        if not isinstance(address, ipaddress.IPv4Address):
            raise TypeError(f"{address} is not an instance of ipaddress.IPv4Address")
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

    @property
    def IP(self) -> ipaddress.IPv4Address:
        return self._IP

    @property
    def response_time(self) -> tuple:
        return self._response_time

    @property
    def all_ports(self):
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
        if isinstance(other, ipaddress.IPv4Address):
            if other == self.IP:
                return True
            return False
        if isinstance(other, FoundDevice):
            if other.IP == self.IP:
                return True
            return False
        if isinstance(other, str):
            try:
                if isinstance(ipaddress.IPv4Address(other), ipaddress.IPv4Address):
                    if ipaddress.IPv4Address(other) == self.IP:
                        return True
                    return False
                else:
                    raise ValueError()
            except ValueError:
                return False
        else:
            return False

    def __repr__(self) -> str:
        # This needs to be expanded and the test updated for it too
        return_string = f"{self.IP} : "
        return_string += f"\n\tresponse times are {self.response_time[0]} ms, {self.response_time[1]} ms, {self.response_time[2]} ms"
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
        return json.dumps(output)

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
        }
        if self.all_ports is not None:
            output[str(self.IP)]["Open_TCP_Ports_List"] = self.open_tcp_ports
            output[str(self.IP)]["Open_UDP_Ports_List"] = self.open_udp_ports
            output[str(self.IP)]["Closed_TCP_Ports_List"] = self.closed_tcp_ports
            output[str(self.IP)]["Closed_UDP_Ports_List"] = self.closed_udp_ports
        return json.dumps(output)


if __name__ == "__main__":
    start_time = time.time()
    address01 = ipaddress.ip_address("192.168.89.80")
    address02 = ipaddress.ip_address("192.168.89.22")
    address03 = ipaddress.ip_address("192.168.1.65")
    address04 = ipaddress.ip_address("10.0.1.254")
    address05 = ipaddress.ip_address("192.168.1.254")
    response_time01 = (1.1, 1.35, 1.82)
    response_time02 = (1.2, 1.35, 1.82)
    response_time03 = (1.3, 1.35, 1.82)
    response_time04 = (1.4, 1.35, 1.82)
    response_time05 = (1.5, 1.35, 1.82)
    ports01 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "25": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "43": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "Domain_Name": "test.local",
                "Server": "192.168.89.80",
                "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                "ns": "[ns 604800 IN A 192.168.89.80]",
                "www": "[www 604800 IN A 192.168.89.80]",
            },
            "79": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "80": {
                "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:42:50 GMT",
                "ETag": '"2ab2-5bc061fadc9e7-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3147",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
            "88": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "109": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "110": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "115": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "118": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "143": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "162": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "179": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "194": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "443": {
                "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:43:27 GMT",
                "ETag": '"2ab0-5bc0621d8c961-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3145",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
            "464": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "465": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "515": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "530": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "543": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "544": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "547": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "993": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "995": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "1080": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3128": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3306": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5432": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5900": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5938": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "8080": {
                "Date": "Tue, 09 Mar 2021 13:09:45 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:51:02 GMT",
                "ETag": '"2abf-5bc063cf93aac-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3157",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
            "8443": {
                "Date": "Tue, 09 Mar 2021 13:09:44 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Mon, 08 Mar 2021 18:24:30 GMT",
                "ETag": '"2abf-5bd0a8b7734dc-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3159",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "Name": "test.local.",
                "Record Type": "SOA",
                "Record Class": "IN",
                "nameserver": "192.168.89.80",
                "port": "53",
                "Answer": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "Canonical Name": "test.local.",
                "Minimum TTL": "604800",
                "CNAMES": [],
                "DNS Record Set": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "expiration": "1615900227.7461846",
            },
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }
    ports02 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "22": {"Return Information": "SSH-1.99-Cisco-1.25"},
            "23": {
                "ERROR": "UnicodeDecodeError -- 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
            },
            "25": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "43": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "79": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "80": {
                "Server": "nginx",
                "Date": "Tue, 09 Mar 2021 13:13:25 GMT",
                "Content-Type": "text/html; charset=utf-8",
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Expires": "Tue, 09 Mar 2021 13:13:25 GMT",
                "Last-Modified": "Tue, 09 Mar 2021 13:13:25 GMT",
                "Cache-Control": "no-store, no-cache, must-revalidate",
                "Pragma": "no-cache",
                "Accept-Ranges": "none",
                "X-XSS-Protection": "1; mode=block",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "SAMEORIGIN",
            },
            "88": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "109": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "110": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "115": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "118": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "143": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "162": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "179": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "194": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "443": {
                "Server": "nginx",
                "Date": "Tue, 09 Mar 2021 13:13:26 GMT",
                "Content-Type": "text/html; charset=utf-8",
                "Transfer-Encoding": "chunked",
                "Connection": "keep-alive",
                "Expires": "Tue, 09 Mar 2021 13:13:26 GMT",
                "Last-Modified": "Tue, 09 Mar 2021 13:13:26 GMT",
                "Cache-Control": "no-store, no-cache, must-revalidate",
                "Pragma": "no-cache",
                "Accept-Ranges": "none",
                "X-XSS-Protection": "1; mode=block",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "SAMEORIGIN",
                "Strict-Transport-Security": "max-age=7884000",
            },
            "464": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "465": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "515": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "530": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "543": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "544": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "547": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "993": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "995": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "1080": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3128": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3306": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5432": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5900": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5938": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "8080": {
                "ERROR": "ConnectionError -- HTTPConnectionPool(host='192.168.89.22', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x036D64A8>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
            "8443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='192.168.89.22', port=8443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x043243A0>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "ERROR": "DNSTimeOutDNS -- operation timed out.  Port is more than likely blocked or not open"
            },
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }
    ports03 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {
                "Return Information": "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------"
            },
            "22": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "25": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "43": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "79": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "80": {
                "Cache-Control": "no-store, no-cache, must-revalidate",
                "Content-Encoding": "gzip",
                "Content-Language": "en",
                "Content-Length": "7124",
                "Content-Type": "text/html; charset=UTF-8",
                "Date": "Tue, 09 Mar 2021 12:51:24 GMT",
                "Expires": "Thu, 19 Nov 1981 08:52:00 GMT",
                "Pragma": "no-cache",
                "Set-Cookie": "PHPSESSID=%2C7ftSWN0xleUHHb-3zISuKKhs2lH-VJBjR-qRx9IPddWkFfqS23w%2CUyiVwOOUmrMil0pIY9MLHrvq7fRfZJBTWHOycXc5f4KtYbqeXE-PNDg3WuMGE44-xPUK5KaWUuG; path=/; HttpOnly; SameSite=Strict",
                "Vary": "Accept-Encoding",
                "X-Frame-Options": "sameorigin",
            },
            "88": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "109": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "110": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "115": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "118": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "143": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "162": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "179": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "194": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='192.168.1.65', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x03F663A0>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
            "464": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "465": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "515": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "530": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "543": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "544": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "547": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "993": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "995": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "1080": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3128": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3306": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5432": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5900": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5938": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "8080": {
                "ERROR": "ConnectionError -- HTTPConnectionPool(host='192.168.1.65', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x03F14478>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
            "8443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='192.168.1.65', port=8443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0450F400>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "ERROR": "DNSTimeOutDNS -- operation timed out.  Port is more than likely blocked or not open"
            },
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }
    ports04 = {
        "TCP": {
            "20": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "21": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "22": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "23": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "25": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "37": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "43": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "53": {"ERROR": "TimeoutError -- [Errno 10060] Unknown error"},
            "79": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "80": {
                "ERROR": "ConnectionError -- HTTPConnectionPool(host='10.0.1.254', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x03B73490>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))"
            },
            "88": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "109": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "110": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "115": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "118": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "143": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "162": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "179": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "194": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "389": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='10.0.1.254', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x03DE63B8>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))"
            },
            "464": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "465": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "515": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "530": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "543": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "544": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "547": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "993": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "995": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "1080": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "3128": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "3306": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "3389": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "5432": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "5900": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "5938": {
                "ERROR": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond"
            },
            "8080": {
                "ERROR": "ConnectionError -- HTTPConnectionPool(host='10.0.1.254', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x00554490>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))"
            },
            "8443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='10.0.1.254', port=8443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x007443D0>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))"
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "ERROR": "DNSTimeOutDNS -- operation timed out.  Port is more than likely blocked or not open"
            },
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }
    ports05 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": ""},
            "22": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "25": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "43": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "79": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "80": {
                "Date": "Tue, 09 Mar 2021 13:11:01 GMT",
                "Server": "2wire Gateway",
                "Content-Type": "text/html",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Transfer-Encoding": "chunked",
                "Pragma": "no-cache",
                "Connection": "Keep-Alive",
            },
            "88": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "109": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "110": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "115": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "118": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "143": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "162": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "179": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "194": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "443": {
                "Date": "Tue, 09 Mar 2021 13:11:06 GMT",
                "Server": "2wire Gateway",
                "Content-Type": "text/html",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Transfer-Encoding": "chunked",
                "Pragma": "no-cache",
                "Connection": "Keep-Alive",
            },
            "464": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "465": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "515": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "530": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "543": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "544": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "547": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "993": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "995": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "1080": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3128": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3306": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5432": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5900": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5938": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "8080": {
                "ERROR": "ConnectionError -- HTTPConnectionPool(host='192.168.1.254', port=8080): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x03A94478>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
            "8443": {
                "ERROR": "ConnectionError -- HTTPSConnectionPool(host='192.168.1.254', port=8443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x040C43B8>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))"
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "Name": "test.local.",
                "Record Type": "SOA",
                "Record Class": "IN",
                "nameserver": "192.168.1.254",
                "port": "53",
                "Answer": "test.local. 900 IN SOA ns1-etm.att.net. nomail.etm.att.net. 1 604800 3600 2419200 900",
                "Canonical Name": "test.local.",
                "Minimum TTL": "900",
                "CNAMES": [],
                "DNS Record Set": "test.local. 900 IN SOA ns1-etm.att.net. nomail.etm.att.net. 1 604800 3600 2419200 900",
                "expiration": "1615296406.0719643",
            },
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }

    test_device01 = FoundDevice(address01, response_time01)
    test_device02 = FoundDevice(address02, response_time02)
    test_device03 = FoundDevice(address03, response_time03)
    test_device04 = FoundDevice(address04, response_time04)
    test_device01.all_ports = ports01
    test_device02.all_ports = ports02
    test_device03.all_ports = ports03
    test_device04.all_ports = ports04
    print(repr(test_device01))
    print(repr(test_device02))
    print(repr(test_device03))
    print(repr(test_device04))
    print(test_device01)
    print(test_device02)
    print(test_device03)
    print(test_device04)
    print(test_device01.print_json_short())
    print("\n\n\n\n")
    print(test_device01.print_json_long())
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")