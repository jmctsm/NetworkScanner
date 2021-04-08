import re
import unittest
import ipaddress
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from scan_mods.mp_pinger import pinger
from scan_mods.mp_pinger import __ping_address as ping_address


class TestPinger(unittest.TestCase):
    """
    Tests that pinger works
    """

    test_addresses = [
        ipaddress.ip_network("192.168.1.64/29"),
        ipaddress.ip_network("10.0.1.0/29"),
        ipaddress.ip_network("192.168.89.0/24"),
        ipaddress.ip_address("192.168.1.65"),
    ]
    test_networks = [
        ipaddress.ip_network("192.168.1.64/29"),
        ipaddress.ip_network("10.0.1.0/29"),
        ipaddress.ip_network("10.0.1.0/29"),
        ipaddress.ip_network("192.168.89.0/24"),
    ]

    def test_00_all_pass_pinger(self):
        print("\nStart testing that all pass")
        for address in self.test_addresses:
            hosts_lists = []
            if isinstance(address, ipaddress.IPv4Network):
                for x in address.hosts():
                    hosts_lists.append(x)
            elif isinstance(address, ipaddress.IPv4Address):
                hosts_lists.append(address)
            active_hosts = pinger(hosts_lists)
            self.assertGreaterEqual(len(active_hosts), 0)
            self.assertIsInstance(active_hosts, dict)
            for key in active_hosts.keys():
                self.assertIsInstance(active_hosts[key], dict)
                self.assertIsInstance(active_hosts[key]["ping"], tuple)
                self.assertEqual(len(active_hosts[key]["ping"]), 3)
            print(f"Tests passed for network/address {str(address)}")
        print("Finish testing that all pass\n")

    def test_01_all_pass_ping_address(self):
        print("\nStart testing that all pass")
        for address in self.test_addresses:
            hosts_lists = []
            if isinstance(address, ipaddress.IPv4Network):
                for x in address.hosts():
                    hosts_lists.append(x)
            elif isinstance(address, ipaddress.IPv4Address):
                hosts_lists.append(address)
            for host in hosts_lists:
                return_value = ping_address(host)
                self.assertTrue(
                    isinstance(return_value, tuple) or isinstance(return_value, str)
                )
                if isinstance(return_value, str):
                    self.assertEqual(return_value, "TIMEOUT")
                if isinstance(return_value, tuple):
                    self.assertIsInstance(return_value[0], ipaddress.IPv4Address)
                    self.assertEqual(return_value[0], host)
                    self.assertIsInstance(return_value[1], tuple)
                    self.assertEqual(len(return_value[1]), 3)
                    self.assertIsInstance(return_value[1][0], float)
                    self.assertIsInstance(return_value[1][1], float)
                    self.assertIsInstance(return_value[1][2], float)
            print(f"Tests passed for network/address {str(address)}")
        print("Finish testing that all pass\n")

    def test_02_pinger_fail_as_expected(self):
        print("\nStart testing that all fail due to empty list passed")
        test_list = []
        with self.assertRaises(ValueError):
            pinger(test_list)
        print("Finish testing that all fail due to empty list passed\n")
        print("\nStart testing that all fail due to not a list passed")
        for address in self.test_networks:
            hosts_lists = []
            for x in address.hosts():
                hosts_lists.append(x)
            with self.assertRaises(TypeError):
                pinger(tuple(hosts_lists))
        print("Finish testing that all fail due to not a list passed\n")
        print("\nStart testing that all fail due to no subnets.  All host bits")
        with self.assertRaises(ValueError):
            test_02_addresses = [
                ipaddress.ip_network("192.168.1.65/29"),
                ipaddress.ip_network("10.0.1.248/32"),
            ]
            for address in test_02_addresses:
                pinger(address)
        print("Finish testing that all fail due to no subnets.  All host bits\n")

    def test_03_pass_due_to_no_active_hosts(self):
        print("\nStart testing that passed due to no active hosts")
        test_addresses = [
            ipaddress.ip_network("192.168.1.0/29"),
            ipaddress.ip_network("10.0.1.16/29"),
        ]
        for address in test_addresses:
            hosts_lists = []
            for x in address.hosts():
                hosts_lists.append(x)
            with self.assertRaises(Exception):
                pinger(hosts_lists)
        print("Finish testing that passed due to no active hosts\n")

    def test_04_pass_due_to_no_arguments_passed_to_pinger(self):
        print("\nStart testing that all fail due to no arguments passed\n")
        with self.assertRaises(TypeError):
            pinger()
        print("\nFinish testing that all fail due to no arguments passed\n")

    def test_05_fail_due_to_no_not_an_IP_to_pinger(self):
        print("\nStart testing that pinger fails due to an IP not being in the list\n")
        test_addresses = [
            ipaddress.ip_address("10.0.1.254"),
            ipaddress.ip_address("192.168.1.65"),
            "abc",
            123,
        ]
        with self.assertRaises(ValueError):
            pinger(test_addresses)
        print("\nFinish testing that pinger fails due to an IP not being in the list\n")

    def test_06_fail_due_to_no_not_an_IP_to_ping_address(self):
        print("\nStart testing that pinger fails due to an IP not being in the list\n")
        test_addresses = [
            "10.0.1.254",
            ipaddress.ip_network("10.0.1.16/29"),
            "abc",
            123,
        ]
        with self.assertRaises(ValueError):
            for address in test_addresses:
                ping_address(address)
        print("\nFinish testing that pinger fails due to an IP not being in the list\n")


if __name__ == "__main__":
    unittest.main()