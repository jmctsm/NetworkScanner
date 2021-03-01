#!python

import unittest
import os
import sys
import ipaddress

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import scan_mods.protocol_scanners.dns_scanner


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

    def test_00__validate_server_domainname_function_all_pass(self):
        """
        Tests that the validate function returns correctly when good values are passed in
        """
        print(
            "\nStarting the test for the validation function when all good values are passed in..."
        )
        for server in self.test_servers:
            for domainname in self.local_domain_name:
                result = (
                    scan_mods.protocol_scanners.dns_scanner.validate_server_domain_name(
                        server, domainname
                    )
                )
                self.assertIsInstance(result, tuple)
                self.assertTupleEqual(result, (server, domainname))
                self.assertEqual(result[0], server)
                self.assertEqual(result[1], domainname)
                result = (
                    scan_mods.protocol_scanners.dns_scanner.validate_server_domain_name(
                        server=None, domain_name=domainname
                    )
                )
                self.assertIsInstance(result, tuple)
                self.assertTupleEqual(result, ("192.168.89.80", domainname))
                self.assertEqual(result[0], "192.168.89.80")
                self.assertEqual(result[1], domainname)
                result = (
                    scan_mods.protocol_scanners.dns_scanner.validate_server_domain_name(
                        server, domain_name=None
                    )
                )
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
                scan_mods.protocol_scanners.dns_scanner.validate_server_domain_name(
                    server=bad_server_value, domain_name=None
                )
        for bad_domain_value in bad_domain_values:
            with self.assertRaises(ValueError):
                scan_mods.protocol_scanners.dns_scanner.validate_server_domain_name(
                    server=None, domain_name=bad_domain_value
                )
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
                self.assertIsInstance(result, str)
                result = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    domainname=domain
                )
                self.assertIsInstance(result, str)
                result = scan_mods.protocol_scanners.dns_scanner.udp_dns_scanner(
                    dns_server=server
                )
                self.assertIsInstance(result, str)

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
                print(result)
                self.assertIsInstance(result, str)
                result = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    domainname=domain
                )
                self.assertIsInstance(result, str)
                result = scan_mods.protocol_scanners.dns_scanner.tcp_dns_scanner(
                    dns_server=server
                )
                self.assertIsInstance(result, str)

        print(
            "Finished the test for the tcp_dns_scanner function passed correctly...\n"
        )


if __name__ == "__main__":
    unittest.main()