#!python

from typing import Type
import unittest
import os
import sys
import ipaddress
import json

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from scan_mods.protocol_scanners.http_scanner import http_scanner


class TestPortScanner(unittest.TestCase):
    """
    Tests that HTTP port scanner works
    """

    test_good_ports = [80, 8080, None]

    def test_00_all_pass_using_http_scanner(self):
        """
        Tests that the HTTP port scanner passes initial tests
        """
        print("\nStarting test for all pass with http_scanner")
        for address in [
            "192.168.1.65",
            "10.0.1.1",
            "192.168.89.80",
            "192.168.1.254",
            "192.168.89.1",
        ]:
            for port in self.test_good_ports:
                result = http_scanner(address, port)
                self.assertIsNotNone(result)
                self.assertGreaterEqual(len(result), 1)
                self.assertIsInstance(result, dict)
                for key in result.keys():
                    self.assertIsInstance(key, str)
        print("Finished test for all pass with http_scanner\n")

    def test_01_pass_non_string_and_fail(self):
        """
        Tests that the HTTP port scanner fails when passed a non-string value
        """
        print("\nStarting test for http_scanner failing for using a non-string")
        for address in [
            1,
            [1, 2],
            (1, 2),
            1.1,
            {"test": "test"},
        ]:
            with self.assertRaises(TypeError):
                http_scanner(address)
        print("Finished test for http_scanner failing for using a non-string\n")

    def test_02_pass_non_IPv4able_arg_and_fail(self):
        """
        Tests that the HTTP port scanner fails when passed a non-IPv4-able string
        """
        print(
            "\nStarting test for http_scanner failing for using a non_IP-able address"
        )
        for address in ["1.1.1", "1", "a"]:
            with self.assertRaises(ipaddress.AddressValueError):
                http_scanner(address)
        print(
            "Finished test for http_scanner failing for using a non_IP-able address\n"
        )

    def test_03_can_create_valid_json(self):
        """
        Tests that the HTTP port scanner can create valid json
        """
        print("\nStarting test http_scanner can create valid JSON")
        dict_of_results = {}
        for address in [
            "192.168.1.65",
            "10.0.1.1",
            "192.168.89.80",
            "192.168.1.254",
            "192.168.89.1",
        ]:
            dict_of_results[address] = http_scanner(address)
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        print("Finished test http_scanner can create valid JSON\n")

    def test_04_pass_bad_port_value_and_fail(self):
        """
        Tests that the HTTP port scanner fails when passed bad port value
        """
        print("\nStarting test for http_scanner failing when use a bad port value")
        for address in ["1.1.1", "1", "a"]:
            with self.assertRaises(ipaddress.AddressValueError):
                http_scanner(address)
        for address in [
            "192.168.1.65",
            "10.0.1.1",
            "192.168.89.80",
            "192.168.1.254",
            "192.168.89.1",
        ]:

            for port in [
                "a",
            ]:
                with self.assertRaises(ValueError):
                    http_scanner(address, port)
            for port in [
                1.1,
                (1, 1),
                [1, 1],
            ]:
                with self.assertRaises(TypeError):
                    http_scanner(address, port)

            for port in [
                -1,
                1_000_000,
                65536,
            ]:
                with self.assertRaises(ValueError):
                    http_scanner(address, port)

        print("Finished test for http_scanner failing when use a bad port value\n")


if __name__ == "__main__":
    unittest.main()