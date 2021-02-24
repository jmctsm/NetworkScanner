#!python

"""
    This is a class for the devices that are being scanned in the NetworkScanner application
"""

import ipaddress


class FoundDevice:
    """
    Class to define the devices being scanned

    Attributes:
        ._IP = IPv4 object for the IP being scanned
        ._response_time = response time tuple from pinger
        ._open_ports = dict of open ports and headers

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
        self._IP = address
        self._response_time = time_tuple

    @property
    def IP(self) -> ipaddress.IPv4Address:
        return self._IP

    @property
    def response_time(self) -> tuple:
        return self._response_time

    def __hash__(self) -> int:
        return hash(self.IP)

    def __bool__(self) -> bool:
        return bool(self.IP)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, FoundDevice):
            if other.IP == self.IP:
                return True
            return False
        else:
            raise TypeError(f"{other} is not a type of class FoundDevice")

    def __repr__(self) -> str:
        # THis needs to be expanded and the test updated for it too
        return f"{self.IP} : response times are {self.response_time[0]} ms, {self.response_time[1]} ms, {self.response_time[2]} ms"

    """
        TODO:
        __repr__ is ip and other information like response times
        __str__ is ip of the device
        rich comparison operators will return a notimplemented
    """