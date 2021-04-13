#!python

from unittest.mock import patch
import requests
import unittest
import os
import sys
import ipaddress
import json

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

import scan_mods.protocol_scanners.http_scanner


class TestPortScanner(unittest.TestCase):
    """
    Tests that HTTP port scanner works
    """

    good_ports = [80, 8080, None]
    good_servers = [
        "192.168.0.254",
        "192.168.89.80",
        "192.168.89.254",
        "192.168.89.251",
    ]

    def test_01_all_pass_using_http_scanner(self):
        """
        Tests that the HTTP port scanner passes initial tests
        """
        print("\nStarting test for all pass with http_scanner")
        for address in self.good_servers:
            for port in self.good_ports:
                print(f"Scanning {address}:{port}")
                result = scan_mods.protocol_scanners.http_scanner.http_scanner(
                    address, port
                )
                self.assertIsNotNone(result)
                self.assertGreaterEqual(len(result), 1)
                self.assertIsInstance(result, dict)
                for key in result.keys():
                    self.assertIsInstance(key, str)
        print("Finished test for all pass with http_scanner\n")

    def test_02_pass_non_string_and_fail(self):
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
                scan_mods.protocol_scanners.http_scanner.http_scanner(address)
        print("Finished test for http_scanner failing for using a non-string\n")

    def test_03_pass_non_IPv4able_arg_and_fail(self):
        """
        Tests that the HTTP port scanner fails when passed a non-IPv4-able string
        """
        print(
            "\nStarting test for http_scanner failing for using a non_IP-able address"
        )
        for address in ["1.1.1", "1", "a"]:
            with self.assertRaises(ipaddress.AddressValueError):
                scan_mods.protocol_scanners.http_scanner.http_scanner(address)
        print(
            "Finished test for http_scanner failing for using a non_IP-able address\n"
        )

    def test_04_pass_bad_port_value_and_fail(self):
        """
        Tests that the HTTP port scanner fails when passed bad port value
        """
        print("\nStarting test for http_scanner failing when use a bad port value")
        for address in self.good_servers:
            for port in [
                "a",
            ]:
                with self.assertRaises(ValueError):
                    scan_mods.protocol_scanners.http_scanner.http_scanner(address, port)
            for port in [
                1.1,
                (1, 1),
                [1, 1],
            ]:
                with self.assertRaises(TypeError):
                    scan_mods.protocol_scanners.http_scanner.http_scanner(address, port)

            for port in [
                -1,
                1_000_000,
                65536,
            ]:
                with self.assertRaises(ValueError):
                    scan_mods.protocol_scanners.http_scanner.http_scanner(address, port)

        print("Finished test for http_scanner failing when use a bad port value\n")

    @patch.object(requests.Session, "get", side_effect=requests.exceptions.HTTPError)
    def test_05_http_error_catching(
        self,
        mock_requests,
    ):
        """ Tests that the HTTP Error code is caught correctly"""
        print("\nStarting test for http_scanner correctly catching a HTTP Error")
        result = scan_mods.protocol_scanners.http_scanner.http_scanner(
            "192.168.89.80",
            port=80,
        )
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 1)
        self.assertIsInstance(result, dict)
        for key in result.keys():
            self.assertIsInstance(key, str)
            self.assertEqual(key, "ERROR")
            self.assertEqual(result[key], "HTTPError -- ")

        print("Finished test for http_scanner correctly catching a HTTP Error\n")

    @patch.object(
        requests.Session, "get", side_effect=requests.exceptions.ConnectionError
    )
    def test_06_conn_error_catching(
        self,
        mock_requests,
    ):
        """ Tests that the Connection Error code is caught correctly"""
        print("\nStarting test for http_scanner correctly catching a Connection Error")
        result = scan_mods.protocol_scanners.http_scanner.http_scanner(
            "192.168.89.80",
            port=80,
        )
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 1)
        self.assertIsInstance(result, dict)
        for key in result.keys():
            self.assertIsInstance(key, str)
            self.assertEqual(key, "ERROR")
            self.assertEqual(result[key], "ConnectionError -- ")

        print("Finished test for http_scanner correctly catching a Connection Error\n")

    @patch.object(requests.Session, "get", side_effect=Exception)
    def test_07_all_other_error_catching(
        self,
        mock_requests,
    ):
        """ Tests that the any Exception code is caught correctly"""
        print("\nStarting test for http_scanner correctly catching any Exception Error")
        result = scan_mods.protocol_scanners.http_scanner.http_scanner(
            "192.168.89.80",
            port=80,
        )
        self.assertIsNotNone(result)
        self.assertGreaterEqual(len(result), 1)
        self.assertIsInstance(result, dict)
        for key in result.keys():
            self.assertIsInstance(key, str)
            self.assertEqual(key, "ERROR")
            self.assertEqual(result[key], "OtherError -- ")

        print("Finished test for http_scanner correctly catching any Exception Error\n")

    def test_08_can_create_valid_json(self):
        """
        Tests that the HTTP port scanner can create valid json
        """
        print("\nStarting test http_scanner can create valid JSON")
        dict_of_results = {}
        for address in self.good_servers:
            dict_of_results[
                address
            ] = scan_mods.protocol_scanners.http_scanner.http_scanner(address)
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        print("Finished test http_scanner can create valid JSON\n")


if __name__ == "__main__":
    unittest.main()