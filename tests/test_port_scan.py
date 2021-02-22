#!python

from socket import AddressFamily
import unittest
import ipaddress
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from port_scanner import port_scanner
from port_scanner import tcp_scanner
from port_scanner import udp_scanner


class TestPortScanner(unittest.TestCase):
    """
    Tests that port scanner works
    """

    def test_00_all_pass_using_port_scanner(self):
        test_addresses = [
            ipaddress.IPv4Address("192.168.1.65"),
            ipaddress.IPv4Address("10.0.1.254"),
        ]
        for test_address in test_addresses:
            test_result_dict = port_scanner(test_address)
            for key, value in test_result_dict.items():
                message = f"{test_result_dict[key]} is None"
                self.assertIsNotNone(value, message)


"""
    TODO:
        all pass making sure that a dict comes back from port_scanner
        test what comes back from tcp scanner
        test what comes back from udp scanner
        pass bad info into tcp scanner
            port and address
        pass bad info into ud scanner
            port and address
        check that all values come back with a string on them

"""


if __name__ == "__main__":
    unittest.main()