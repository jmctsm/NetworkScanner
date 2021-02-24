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

    test_ipv4_addresses = [
        ipaddress.IPv4Address("192.168.1.65"),
        ipaddress.IPv4Address("10.0.1.254"),
        ipaddress.IPv4Address("192.168.89.80"),
    ]
    test_str_addresses = [
        "192.168.1.65",
        "10.0.1.254",
        "192.168.89.80",
    ]

    def test_00_all_pass_using_port_scanner(self):
        """
        Tests that the port_scanner function passes correctly
        """
        for test_address in self.test_ipv4_addresses:
            test_result_dict = port_scanner(test_address)
            for key, value in test_result_dict.items():
                message = f"{test_result_dict[key]} is None"
                self.assertIsNotNone(value, message)
                self.assertIsInstance(value, str)
                self.assertGreaterEqual(len(value), 1)

    def test_01_tcp_scanner(self):
        """
        Tests that the tcp_scanner function correctly passes
        """
        test_ports = (20, 21, 22, 23, 80)
        for test_address in self.test_str_addresses:
            for test_port in test_ports:
                test_result = tcp_scanner(test_address, test_port)
                message = f"{test_address}:{test_port} returned None"
                self.assertIsNotNone(test_result, message)
                self.assertIsInstance(test_result, str)
                self.assertGreaterEqual(len(test_result), 1)

    def test_02_udp_scanner(self):
        """
        Tests that the udp_scanner function correctly passes
        """
        test_ports = (53, 67, 69, 123)
        for test_address in self.test_str_addresses:
            for test_port in test_ports:
                test_result = udp_scanner(test_address, test_port)
                message = f"{test_address}:{test_port} returned None"
                self.assertIsNotNone(test_result, message)
                self.assertIsInstance(test_result, str)
                self.assertGreaterEqual(len(test_result), 1)

    def test_03_tcp_scanner(self):
        """
        Tests that the tcp_scanner function fails when address is the wrong type
        """
        test_addresses = (ipaddress.IPv4Address("192.168.1.65"), 1, 1.1, (1, 1), [1, 2])
        test_ports = (20, 21, 22, 23, 80)
        for test_address in test_addresses:
            for test_port in test_ports:
                with self.assertRaises(ValueError):
                    tcp_scanner(test_address, test_port)

    def test_04_tcp_scanner(self):
        """
        Tests that the tcp_scanner function fails when port is the wrong type
        """
        test_ports = ("80", 1.1, (1, 1), [1, 2])
        for test_address in self.test_str_addresses:
            for test_port in test_ports:
                with self.assertRaises(ValueError):
                    tcp_scanner(test_address, test_port)

    def test_05_udp_scanner_fails(self):
        """
        Tests that the udp_scanner function fails when address is the wrong type
        """
        test_addresses = (ipaddress.IPv4Address("192.168.1.65"), 1, 1.1, (1, 1), [1, 2])
        test_ports = (20, 21, 22, 23, 80)
        for test_address in test_addresses:
            for test_port in test_ports:
                with self.assertRaises(ValueError):
                    udp_scanner(test_address, test_port)

    def test_06_udp_scanner_fails(self):
        """
        Tests that the udp_scanner function fails when port is the wrong type
        """
        test_ports = ("80", 1.1, (1, 1), [1, 2])
        for test_address in self.test_str_addresses:
            for test_port in test_ports:
                with self.assertRaises(ValueError):
                    udp_scanner(test_address, test_port)


if __name__ == "__main__":
    unittest.main()