#!python

import unittest
import os
import sys
import ipaddress
import json

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from scan_mods.protocol_scanners.https_scanner import https_scanner

# Disable the SSL warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestPortScanner(unittest.TestCase):
    """
    Tests that HTTPS port scanner works
    """

    def test_00_all_pass_using_https_scanner(self):
        """
        Tests that the HTTPS port scanner passes initial tests
        """
        print("\nStarting test for all pass with https_scanner")
        for address in [
            "192.168.1.65",
            "10.0.1.1",
            "192.168.89.80",
            "192.168.1.254",
            "192.168.89.1",
        ]:
            result = https_scanner(address)
            self.assertIsNotNone(result)
            self.assertGreaterEqual(len(result), 1)
            self.assertIsInstance(result, dict)
            for key in result.keys():
                self.assertIsInstance(key, str)
        print("Finished test for all pass with http_scanner\n")

    def test_01_pass_non_string_and_fail(self):
        """
        Tests that the HTTPS port scanner fails when passed a non-string value
        """
        print("\nStarting test for https_scanner failing for using a non-string")
        for address in [
            1,
            [1, 2],
            (1, 2),
            1.1,
            {"test": "test"},
        ]:
            with self.assertRaises(TypeError):
                https_scanner(address)
        print("Finished test for https_scanner failing for using a non-string\n")

    def test_02_pass_non_IPv4able_arg_and_fail(self):
        """
        Tests that the HTTPS port scanner fails when passed a non-IPv4-able string
        """
        print(
            "\nStarting test for https_scanner failing for using a non_IP-able address"
        )
        for address in ["1.1.1", "1", "a"]:
            with self.assertRaises(ipaddress.AddressValueError):
                https_scanner(address)
        print(
            "Finished test for https_scanner failing for using a non_IP-able address\n"
        )

    def test_03_can_create_valid_json(self):
        """
        Tests that the HTTPS port scanner can create valid json
        """
        print("\nStarting test https_scanner can create valid JSON")
        dict_of_results = {}
        for address in [
            "192.168.1.65",
            "10.0.1.1",
            "192.168.89.80",
            "192.168.1.254",
            "192.168.89.1",
        ]:
            dict_of_results[address] = https_scanner(address)
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        print("Finished test https_scanner can create valid JSON\n")


if __name__ == "__main__":
    unittest.main()