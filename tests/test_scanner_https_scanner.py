#!python

import unittest
import os
import sys
import ipaddress

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from protocol_scanners.https_scanner import https_scanner

# Disable the SSL warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestPortScanner(unittest.TestCase):
    """
    Tests that HTTP port scanner works
    """

    def test_00_all_pass_using_http_scanner(self):
        """
        Tests that the HTTP port scanner passes initial tests
        """
        # for address in ["192.168.1.65", "10.0.1.254", "192.168.89.80"]:
        for address in ["192.168.1.65", "10.0.1.254", "192.168.89.80"]:
            result = https_scanner(address)
            self.assertIsNotNone(result)
            self.assertGreaterEqual(len(result), 1)
            self.assertIsInstance(result, str)

    def test_02_pass_non_string_and_fail(self):
        """
        Tests that the HTTPS port scanner fails when passed a non-string value
        """
        for address in [
            1,
            [1, 2],
            (1, 2),
            1.1,
            {"test": "test"},
        ]:
            with self.assertRaises(TypeError):
                result = https_scanner(address)

    def test_03_pass_non_IPv4able_arg_and_fail(self):
        """
        Tests that the HTTPs port scanner fails when passed a non-IPv4-able string
        """
        for address in ["1.1.1", "1", "a"]:
            with self.assertRaises(ipaddress.AddressValueError):
                result = https_scanner(address)


if __name__ == "__main__":
    unittest.main()