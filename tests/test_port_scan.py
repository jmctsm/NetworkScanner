#!python

from socket import AddressFamily
import unittest
import ipaddress
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from scan_mods.port_scanner import port_scanner
from scan_mods.port_scanner import tcp_scanner
from scan_mods.port_scanner import udp_scanner
from scan_mods.port_scanner import __validate_for_scanners as validate


class TestPortScanner(unittest.TestCase):
    """
    Tests that port scanner works
    """

    test_ipv4_addresses = [
        ipaddress.IPv4Address("192.168.1.65"),
        ipaddress.IPv4Address("10.0.1.1"),
        ipaddress.IPv4Address("192.168.89.80"),
        ipaddress.IPv4Address("192.168.1.254"),
    ]
    test_str_addresses = [
        "192.168.1.65",
        "10.0.1.254",
        "192.168.89.80",
    ]
    test_domain_names = [
        "test.local",
        "www.google.com",
        "google.com",
        "test.test",
        None,
    ]
    test_TCP_PORTS = (
        20,
        21,
        22,
        23,
        25,
        37,
        43,
        53,
        79,
        80,
        88,
        109,
        110,
        115,
        118,
        143,
        162,
        179,
        194,
        389,
        443,
        464,
        465,
        515,
        530,
        543,
        544,
        547,
        993,
        995,
        1080,
        3128,
        3306,
        3389,
        5432,
        5900,
        5938,
        8080,
    )
    test_UDP_PORTS = (
        43,
        53,
        67,
        69,
        88,
        118,
        123,
        161,
        162,
        194,
        464,
        514,
        530,
        547,
        995,
        1080,
        3389,
        5938,
        8080,
    )
    bad_test_addresses = (ipaddress.IPv4Address("192.168.1.65"), 1, 1.1, (1, 1), [1, 2])
    bad_test_ports = ("80", 1.1, (1, 1), [1, 2])
    bad_domain_names = (1.1, (1, 1), [1, 2])

    def test_00_all_pass_using_port_scanner(self):
        """
        Tests that the port_scanner function passes correctly
        """
        for test_address in self.test_ipv4_addresses:
            for domain_name in self.test_domain_names:
                test_result_dict = port_scanner(
                    address=test_address, domain_name=domain_name
                )
                for key, value in test_result_dict.items():
                    message = f"{test_result_dict[key]} is None"
                    self.assertIsNotNone(value, message)
                    self.assertIsInstance(value, str)
                    self.assertGreaterEqual(len(value), 1)

    def test_01_tcp_scanner(self):
        """
        Tests that the tcp_scanner function correctly passes
        """
        for test_address in self.test_str_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.test_domain_names:
                    test_result = tcp_scanner(
                        test_address, test_port, domain_name=domain_name
                    )
                    message = f"{test_address}:{test_port} returned None"
                    self.assertIsNotNone(test_result, message)
                    self.assertIsInstance(test_result, str)
                    self.assertGreaterEqual(len(test_result), 1)

    def test_02_udp_scanner(self):
        """
        Tests that the udp_scanner function correctly passes
        """
        for test_address in self.test_str_addresses:
            for test_port in self.test_UDP_PORTS:
                for domain_name in self.test_domain_names:
                    test_result = udp_scanner(
                        test_address, test_port, domain_name=domain_name
                    )
                    message = f"{test_address}:{test_port} returned None"
                    self.assertIsNotNone(test_result, message)
                    self.assertIsInstance(test_result, str)
                    self.assertGreaterEqual(len(test_result), 1)

    def test_03_tcp_udp_scanner_raise_exception(self):
        """
        Tests that the tcp_scanner and udp_scanner functions fail when address is the wrong type
        and when the port is the wrong type
        and when the domain is the wrong type
        """
        for bad_test_address in self.bad_test_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.test_domain_names:
                    with self.assertRaises(TypeError):
                        tcp_scanner(
                            bad_test_address, test_port, domain_name=domain_name
                        )
                    with self.assertRaises(TypeError):
                        udp_scanner(
                            bad_test_address, test_port, domain_name=domain_name
                        )
        for test_address in self.test_str_addresses:
            for bad_test_port in self.bad_test_ports:
                for domain_name in self.test_domain_names:
                    with self.assertRaises(TypeError):
                        tcp_scanner(
                            test_address, bad_test_port, domain_name=domain_name
                        )
                    with self.assertRaises(TypeError):
                        udp_scanner(
                            test_address, bad_test_port, domain_name=domain_name
                        )
        for test_address in self.test_str_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.bad_domain_names:
                    with self.assertRaises(TypeError):
                        tcp_scanner(test_address, test_port, domain_name=domain_name)
                    with self.assertRaises(TypeError):
                        udp_scanner(test_address, test_port, domain_name=domain_name)

    def test_04_validate_function_passes(self):
        """
        Tests that the validate function passes when address is the correct type
        and when the port is the correct type
        and when the domain is the correct type
        """
        for test_address in self.test_str_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.test_domain_names:
                    self.assertTrue(validate(test_address, test_port, domain_name))

    def test_05_validate_function_fails(self):
        """
        Tests that the validate function fails fail when address is the wrong type
        and when the port is the wrong type
        and when the domain is the wrong type
        """
        for bad_test_address in self.bad_test_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.test_domain_names:
                    with self.assertRaises(TypeError):
                        validate(bad_test_address, test_port, domain_name=domain_name)
                    with self.assertRaises(TypeError):
                        validate(bad_test_address, test_port, domain_name=domain_name)
        for test_address in self.test_str_addresses:
            for bad_test_port in self.bad_test_ports:
                for domain_name in self.test_domain_names:
                    with self.assertRaises(TypeError):
                        validate(test_address, bad_test_port, domain_name=domain_name)
                    with self.assertRaises(TypeError):
                        validate(test_address, bad_test_port, domain_name=domain_name)
        for test_address in self.test_str_addresses:
            for test_port in self.test_TCP_PORTS:
                for domain_name in self.bad_domain_names:
                    with self.assertRaises(TypeError):
                        validate(test_address, test_port, domain_name=domain_name)
                    with self.assertRaises(TypeError):
                        validate(test_address, test_port, domain_name=domain_name)


if __name__ == "__main__":
    unittest.main()