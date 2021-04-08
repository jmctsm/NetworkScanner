#!python

import unittest
import os
import sys
import ipaddress
import json

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

import scan_mods.protocol_scanners.dns_scanner
from scan_mods.protocol_scanners.dns_scanner import (
    __validate_server_domain_name as validate_server_domain_name,
    __strip_alligators as strip_alligators,
)


class TestPortScanner(unittest.TestCase):
    """
    Tests that DNS port scanner works

    There are no failure tests for the udp and tcp scanners due to the validation function
    """

    test_servers = [
        "192.168.1.65",
        "192.168.89.80",
    ]
    local_domain_name = ["test.local", "www.google.com", "google.com", "test.test"]

    def test_00_validate_server_domainname_function_all_pass(self):
        """
        Tests that the validate function returns correctly when good values are passed in
        """
        print(
            "\nStarting the test for the validation function when all good values are passed in..."
        )
        for server in self.test_servers:
            for domainname in self.local_domain_name:
                result = validate_server_domain_name(server, domainname)
                self.assertIsInstance(result, tuple)
                self.assertTupleEqual(result, (server, domainname))
                self.assertEqual(result[0], server)
                self.assertEqual(result[1], domainname)
                result = validate_server_domain_name(
                    server=None, domain_name=domainname
                )
                self.assertIsInstance(result, tuple)
                self.assertTupleEqual(result, ("192.168.89.80", domainname))
                self.assertEqual(result[0], "192.168.89.80")
                self.assertEqual(result[1], domainname)
                result = validate_server_domain_name(server, domain_name=None)
                self.assertIsInstance(result, tuple)
                self.assertTupleEqual(result, (server, "test.local"))
                self.assertEqual(result[0], server)
                self.assertEqual(result[1], "test.local")
        print(
            "Finished the test for the validation function when all good values are passed in...\n"
        )

    def test_01_validate_failures(self):
        """
        This will make sure the validate function fails correctly
        """
        print(
            "\nStarting the test for the validation function fails with bad values are passed in..."
        )
        bad_server_values = [1, 1.1, (1, 1), {1, 1}, "a", "192.158.1."]
        bad_domain_values = [
            1,
            1.1,
            (1, 1),
            {1, 1},
        ]
        for bad_server_value in bad_server_values:
            with self.assertRaises(ValueError):
                validate_server_domain_name(server=bad_server_value, domain_name=None)
        for bad_domain_value in bad_domain_values:
            with self.assertRaises(ValueError):
                validate_server_domain_name(server=None, domain_name=bad_domain_value)
        print(
            "Finished the test for the validation function fails with bad values are passed in...\n"
        )

    def test_02_udp_dns_scanner_all_pass(self):
        """
        This will make sure the udp_dns_scanner can pass correctly
        """
        print(
            "\nStarting the test for the udp_dns_scanner function passed correctly..."
        )
        for server in self.test_servers:
            for domain in self.local_domain_name:
                result = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    server, domain
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)
                result = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    domainname=domain
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)
                result = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    dns_server=server
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)

        print(
            "Finished the test for the udp_dns_scanner function passed correctly...\n"
        )

    def test_03_tcp_dns_scanner_all_pass(self):
        """
        This will make sure the tcp_dns_scanner can pass correctly
        """
        print(
            "\nStarting the test for the tcp_dns_scanner function passed correctly..."
        )
        for server in self.test_servers:
            for domain in self.local_domain_name:
                result = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    server, domain
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)
                result = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    domainname=domain
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)
                result = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    dns_server=server
                )
                self.assertIsInstance(result, dict)
                self.assertGreaterEqual(len(result), 1)
                for key in result.keys():
                    self.assertIsInstance(key, str)

        print(
            "Finished the test for the tcp_dns_scanner function passed correctly...\n"
        )

    def test_04_strip_alligators_all_pass(self):
        """
        This will test the strip alligators function and make sure that it passes
        """
        print(
            "\nStarting the test for the __strip_alligators function passes correctly..."
        )
        strings_to_test = [
            "<first test>",
            "<<second test>>",
            "<<<third test>>>",
            "<<<fourth test>",
            "fifth test",
            "<sixth test]",
            "[seventh test>",
        ]
        good_values = [
            "[first test]",
            "[[second test]]",
            "[[[third test]]]",
            "[[[fourth test]",
            "fifth test",
            "[sixth test]",
            "[seventh test]",
        ]
        counter = 0
        while counter < len(strings_to_test):
            self.assertEqual(
                strip_alligators(strings_to_test[counter]),
                good_values[counter],
            )
            counter += 1

        print(
            "Finished the test for the __strip_alligators function passes correctly...\n"
        )

    def test_05_strip_alligators_raises_error(self):
        """
        This will test the strip alligators function and make sure that it raises an error
        """
        print(
            "\nStarting the test for the __strip_alligators function raises an error..."
        )

        class Fail_Class:
            def __init__(self):
                self.name = "name"

            def __str__(self):
                raise TypeError

        with self.assertRaises(TypeError):
            strip_alligators(p=Fail_Class())

        print(
            "Finished the test for the __strip_alligators function raises an error...\n"
        )

    def test_06_tcp_udp_can_be_used_in_json(self):
        """
        This will make sure the tcp and udp scanner output can be used in json
        """
        print(
            "\nStarting the test that the udp and tcp scanners output can be used in JSON..."
        )
        dict_of_results = {}
        for server in self.test_servers:
            for domain in self.local_domain_name:
                dict_of_results[
                    f"{str(server)}_UDP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    server, domain
                )
                dict_of_results[
                    f"{str(server)}_TCP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    server, domain
                )
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        dict_of_results = {}
        for server in self.test_servers:
            for domain in self.local_domain_name:
                dict_of_results[
                    f"{str(server)}_UDP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    domainname=domain
                )
                dict_of_results[
                    f"{str(server)}_TCP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    domainname=domain
                )
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        dict_of_results = {}
        for server in self.test_servers:
            for domain in self.local_domain_name:
                dict_of_results[
                    f"{str(server)}_UDP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    dns_server=server
                )
                dict_of_results[
                    f"{str(server)}_TCP_{domain}"
                ] = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    dns_server=server
                )
        json_output = json.dumps(dict_of_results)
        self.assertIsNotNone(json_output)
        self.assertGreaterEqual(len(json_output), 1)
        self.assertIsInstance(json_output, str)
        print(
            "Finished the test that the udp and tcp scanners output can be used in JSON...\n"
        )


if __name__ == "__main__":
    unittest.main()