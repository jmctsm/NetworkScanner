#!python

"""
    This is a class for the devices that are being scanned in the NetworkScanner application
"""

import ipaddress
from os import add_dll_directory
import re
import time
import pprint


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
        self._all_ports = {}
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
            for key in ports_headers.keys():
                if "TCP_" in key or "UDP_" in key:
                    if isinstance(ports_headers[key], str):
                        self._all_ports[key] = ports_headers[key]
                    else:
                        raise TypeError(
                            f"{ports_headers[key]} is not a string.  "
                            f"It was {type(ports_headers[key])}"
                        )
                else:
                    raise ValueError(
                        f"{key} does not follow standard of 'TCP_' or 'UDP_'"
                    )
        else:
            raise TypeError(
                f"ports variable passed in was not a dictionary.  It was {type(ports_headers)}."
                f"You may want to fix that."
            )
        tcp_pattern = "TCP_(.*)"
        udp_pattern = "UDP_(.*)"
        for key in self._all_ports.keys():
            if re.search(tcp_pattern, key):
                tcp_closed_pattern = (
                    "(ConnectionRefusedError|Connection error occurred)"
                )
                if re.search(tcp_closed_pattern, self._all_ports[key]):
                    self._closed_tcp_ports[key] = self._all_ports[key]
                else:
                    self._open_tcp_ports[key] = self._all_ports[key]
            if re.search(udp_pattern, key):
                udp_closed_pattern = "(Socket Timed Out|DNS operation timed out)"
                if re.search(udp_closed_pattern, self._all_ports[key]):
                    self._closed_udp_ports[key] = self._all_ports[key]
                else:
                    self._open_udp_ports[key] = self._all_ports[key]
        try:
            assert len(self._all_ports) == len(self._open_tcp_ports) + len(
                self.closed_tcp_ports
            ) + len(self._open_udp_ports) + len(self.closed_udp_ports)
        except AssertionError:
            raise AssertionError(
                f"The length of the ports categorized does not equal the length of the number of ports for TCP"
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

    @property
    def unknown_tcp_ports(self):
        """
        Getter for the unknown TCP ports for the device
        Return:
            dict : dictionary of the unknown ports in port_number: header
        """
        return self._unknown_tcp_ports

    @property
    def unknown_udp_ports(self):
        """
        Getter for the unknown UDP ports for the device
        Return:
            dict : dictionary of the unknown ports in port_number: header
        """
        return self._unknown_udp_ports

    def __hash__(self) -> int:
        return hash(self.IP)

    def __bool__(self) -> bool:
        return bool(self.IP)

    def __eq__(self, other: object) -> bool:
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
        return f"{self.IP} : response times are {self.response_time[0]} ms, {self.response_time[1]} ms, {self.response_time[2]} ms"

    """
        TODO:
        __repr__ is ip and other information like response times
        __str__ is ip of the device
        rich comparison operators will return a notimplemented
    """


if __name__ == "__main__":
    start_time = time.time()
    address03 = ipaddress.ip_address("192.168.1.65")
    address02 = ipaddress.ip_address("10.0.1.254")
    address01 = ipaddress.ip_address("192.168.89.80")
    address04 = ipaddress.ip_address("192.168.1.254")
    response_time03 = (1.1, 1.35, 1.82)
    response_time02 = (1.2, 1.35, 1.82)
    response_time01 = (1.3, 1.35, 1.82)
    response_time04 = (1.4, 1.35, 1.82)
    ports03 = {
        "TCP_20": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_21": "220---------- Welcome to Pure-FTPd [privsep] [TLS] ----------",
        "TCP_22": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_23": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_25": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_37": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_43": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_53": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_79": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_80": "Server : None Listed in Headers\n\tCache-Control : no-store, no-cache, must-revalidate\n\tContent-Encoding : gzip\n\tContent-Language : en\n\tContent-Length : 7125\n\tContent-Type : text/html; charset=UTF-8\n\tDate : Wed, 03 Mar 2021 18:31:09 GMT\n\tExpires : Thu, 19 Nov 1981 08:52:00 GMT\n\tPragma : no-cache\n\tSet-Cookie : PHPSESSID=rYfmJIkckKt1zQWlH-QVt5hxZb8d6bRCzwpsFiixiiPtmQcj13IMT%2CGaZBfhAWM4hrs0hndjOkBU798QS08q1PIqoDDD-egJzYIXvlKXlRROONiYiZT5qfahHSoeWxHh; path=/; HttpOnly; SameSite=Strict\n\tVary : Accept-Encoding\n\tX-Frame-Options : sameorigin",
        "TCP_88": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_109": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_110": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_115": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_118": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_143": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_162": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_179": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_194": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_443": "Connection error occurred -- HTTPSConnectionPool(host='192.168.1.65', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0422FAC0>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it'))",
        "TCP_464": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_465": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_515": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_530": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_543": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_544": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_547": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_993": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_995": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_1080": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3128": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3306": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5432": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5900": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5938": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_8080": "Server : None Listed in Headers\n\tCache-Control : no-store, no-cache, must-revalidate\n\tContent-Encoding : gzip\n\tContent-Language : en\n\tContent-Length : 7124\n\tContent-Type : text/html; charset=UTF-8\n\tDate : Wed, 03 Mar 2021 18:31:13 GMT\n\tExpires : Thu, 19 Nov 1981 08:52:00 GMT\n\tPragma : no-cache\n\tSet-Cookie : PHPSESSID=0q85U8OF4KX9CDXkhuiwtBPow2PecQuApevcu7M8CD3jc3TP5uZd1G966DN62yHAVgDZBJ7zZ9xpdOmUYjGl2YLQVC6%2Cspe4LqDwjcsNomAHko%2C-d5-NHRw%2CgGplqLfv; path=/; HttpOnly; SameSite=Strict\n\tVary : Accept-Encoding\n\tX-Frame-Options : sameorigin",
        "UDP_43": "Socket Timed Out",
        "UDP_53": "DNS operation timed out.  Port is more than likely blocked or not open",
        "UDP_67": "Socket Timed Out",
        "UDP_69": "Socket Timed Out",
        "UDP_88": "Socket Timed Out",
        "UDP_118": "Socket Timed Out",
        "UDP_123": "Socket Timed Out",
        "UDP_161": "Socket Timed Out",
        "UDP_162": "Socket Timed Out",
        "UDP_194": "Socket Timed Out",
        "UDP_464": "Socket Timed Out",
        "UDP_514": "Socket Timed Out",
        "UDP_530": "Socket Timed Out",
        "UDP_547": "Socket Timed Out",
        "UDP_995": "Socket Timed Out",
        "UDP_1080": "Socket Timed Out",
        "UDP_3389": "Socket Timed Out",
        "UDP_5938": "Socket Timed Out",
        "UDP_8080": "Socket Timed Out",
    }
    ports02 = {
        "TCP_20": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_21": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_22": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_23": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_25": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_37": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_43": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_53": "TimeoutError -- [Errno 10060] Unknown error",
        "TCP_79": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_80": "Connection error occurred -- HTTPConnectionPool(host='10.0.1.254', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x040BFBB0>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))",
        "TCP_88": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_109": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_110": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_115": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_118": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_143": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_162": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_179": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_194": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_389": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_443": "Connection error occurred -- HTTPSConnectionPool(host='10.0.1.254', port=443): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0473FAD8>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))",
        "TCP_464": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_465": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_515": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_530": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_543": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_544": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_547": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_993": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_995": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_1080": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_3128": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_3306": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_3389": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_5432": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_5900": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_5938": "TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond",
        "TCP_8080": "Connection error occurred -- HTTPConnectionPool(host='10.0.1.254', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0391FBB0>: Failed to establish a new connection: [WinError 10060] A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond'))",
        "UDP_43": "Socket Timed Out",
        "UDP_53": "DNS operation timed out.  Port is more than likely blocked or not open",
        "UDP_67": "Socket Timed Out",
        "UDP_69": "Socket Timed Out",
        "UDP_88": "Socket Timed Out",
        "UDP_118": "Socket Timed Out",
        "UDP_123": "Socket Timed Out",
        "UDP_161": "Socket Timed Out",
        "UDP_162": "Socket Timed Out",
        "UDP_194": "Socket Timed Out",
        "UDP_464": "Socket Timed Out",
        "UDP_514": "Socket Timed Out",
        "UDP_530": "Socket Timed Out",
        "UDP_547": "Socket Timed Out",
        "UDP_995": "Socket Timed Out",
        "UDP_1080": "Socket Timed Out",
        "UDP_3389": "Socket Timed Out",
        "UDP_5938": "Socket Timed Out",
        "UDP_8080": "Socket Timed Out",
    }
    ports01 = {
        "TCP_20": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_21": "220 (vsFTPd 3.0.3)",
        "TCP_22": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1",
        "TCP_23": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_25": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_37": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_43": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_53": "Zone transfer for test.local from server 192.168.89.80\n\t@ 604800 IN SOA @ root 2 604800 86400 2419200 604800\n\t@ 604800 IN NS ns\n\t@ 604800 IN A 192.168.89.80\n\t@ 604800 IN AAAA ::1\n\tns 604800 IN A 192.168.89.80\n\twww 604800 IN A 192.168.89.80",
        "TCP_79": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_80": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Wed, 03 Mar 2021 18:48:31 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:42:50 GMT\n\tETag : "2ab2-5bc061fadc9e7-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3147\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
        "TCP_88": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_109": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_110": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_115": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_118": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_143": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_162": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_179": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_194": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_443": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Wed, 03 Mar 2021 18:48:31 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:43:27 GMT\n\tETag : "2ab0-5bc0621d8c961-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3145\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
        "TCP_464": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_465": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_515": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_530": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_543": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_544": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_547": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_993": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_995": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_1080": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3128": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3306": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5432": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5900": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5938": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_8080": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Wed, 03 Mar 2021 18:48:34 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:42:50 GMT\n\tETag : "2ab2-5bc061fadc9e7-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3147\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
        "UDP_43": "Socket Timed Out",
        "UDP_53": "Canonical Name : test.local.\n\tName = test.local.\n\tRecord Type = SOA\n\tRecord Class = IN\n\tnameserver = 192.168.89.80\n\tport = 53\n\tAnswer = test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800\n\tMinimum TTL = 604800\n\tDNS Record Set = test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800\n\texpiration = 1615402157.7862682",
        "UDP_67": "Socket Timed Out",
        "UDP_69": "Socket Timed Out",
        "UDP_88": "Socket Timed Out",
        "UDP_118": "Socket Timed Out",
        "UDP_123": "Socket Timed Out",
        "UDP_161": "Socket Timed Out",
        "UDP_162": "Socket Timed Out",
        "UDP_194": "Socket Timed Out",
        "UDP_464": "Socket Timed Out",
        "UDP_514": "Socket Timed Out",
        "UDP_530": "Socket Timed Out",
        "UDP_547": "Socket Timed Out",
        "UDP_995": "Socket Timed Out",
        "UDP_1080": "Socket Timed Out",
        "UDP_3389": "Socket Timed Out",
        "UDP_5938": "Socket Timed Out",
        "UDP_8080": "Socket Timed Out",
    }
    ports04 = {
        "TCP_20": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_21": "Nothing returned from the server",
        "TCP_22": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_23": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_25": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_37": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_43": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_53": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_79": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_80": "Server : 2wire Gateway\n\tDate : Wed, 03 Mar 2021 18:50:37 GMT\n\tContent-Type : text/html\n\tCache-Control : no-cache, no-store, must-revalidate\n\tTransfer-Encoding : chunked\n\tPragma : no-cache\n\tConnection : Keep-Alive",
        "TCP_88": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_109": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_110": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_115": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_118": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_143": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_162": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_179": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_194": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_443": "Server : 2wire Gateway\n\tDate : Wed, 03 Mar 2021 18:50:48 GMT\n\tContent-Type : text/html\n\tCache-Control : no-cache, no-store, must-revalidate\n\tTransfer-Encoding : chunked\n\tPragma : no-cache\n\tConnection : Keep-Alive",
        "TCP_464": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_465": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_515": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_530": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_543": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_544": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_547": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_993": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_995": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_1080": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3128": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3306": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_3389": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5432": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5900": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_5938": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it",
        "TCP_8080": "Server : 2wire Gateway\n\tDate : Wed, 03 Mar 2021 18:50:42 GMT\n\tContent-Type : text/html\n\tCache-Control : no-cache, no-store, must-revalidate\n\tTransfer-Encoding : chunked\n\tPragma : no-cache\n\tConnection : Keep-Alive",
        "UDP_43": "Socket Timed Out",
        "UDP_53": "Canonical Name : test.local.\n\tName = test.local.\n\tRecord Type = SOA\n\tRecord Class = IN\n\tnameserver = 192.168.1.254\n\tport = 53\n\tAnswer = test.local. 900 IN SOA ns1-etm.att.net. nomail.etm.att.net. 1 604800 3600 2419200 900\n\tMinimum TTL = 900\n\tDNS Record Set = test.local. 900 IN SOA ns1-etm.att.net. nomail.etm.att.net. 1 604800 3600 2419200 900\n\texpiration = 1614798390.681023",
        "UDP_67": "Socket Timed Out",
        "UDP_69": "Socket Timed Out",
        "UDP_88": "Socket Timed Out",
        "UDP_118": "Socket Timed Out",
        "UDP_123": "Socket Timed Out",
        "UDP_161": "Socket Timed Out",
        "UDP_162": "Socket Timed Out",
        "UDP_194": "Socket Timed Out",
        "UDP_464": "Socket Timed Out",
        "UDP_514": "Socket Timed Out",
        "UDP_530": "Socket Timed Out",
        "UDP_547": "Socket Timed Out",
        "UDP_995": "Socket Timed Out",
        "UDP_1080": "Socket Timed Out",
        "UDP_3389": "Socket Timed Out",
        "UDP_5938": "Socket Timed Out",
        "UDP_8080": "Socket Timed Out",
    }

    test_device01 = FoundDevice(address01, response_time01)
    test_device02 = FoundDevice(address02, response_time02)
    test_device03 = FoundDevice(address03, response_time03)
    test_device04 = FoundDevice(address04, response_time04)
    test_device01.all_ports = ports01
    print(f"test_device01.all_ports = {test_device01.all_ports}")
    print(f"test_device01.open_tcp_ports = {test_device01.open_tcp_ports}")
    print(f"test_device01.closed_tcp_ports = {test_device01.closed_tcp_ports}")
    print(f"test_device01.open_udp_ports = {test_device01.open_udp_ports}")
    print(f"test_device01.closed_udp_ports = {test_device01.closed_udp_ports}")

    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")