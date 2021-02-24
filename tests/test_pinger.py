import unittest
import ipaddress
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from pinger import pinger


class TestPinger(unittest.TestCase):
    """
    Tests that pinger works
    """

    def test_00_all_pass(self):
        print("\nStart testing that all pass\n")
        test_addresses = [
            ipaddress.ip_network("192.168.1.64/29"),
            ipaddress.ip_network("10.0.1.248/29"),
            ipaddress.ip_address("192.168.1.65"),
        ]
        for address in test_addresses:
            hosts_lists = []
            if isinstance(address, ipaddress.IPv4Network):
                for x in address.hosts():
                    hosts_lists.append(x)
            elif isinstance(address, ipaddress.IPv4Address):
                hosts_lists.append(address)
            active_hosts = pinger(hosts_lists)
            active_hosts_length = len(active_hosts)
            self.assertGreaterEqual(active_hosts_length, 0)
            print(f"Tests passed for network {str(address)}")
        print("\nFinish testing that all pass\n")

    def test_01_fail_due_to_hosts(self):
        print("\nStart testing that all fail due to no subnets.  All host bits\n")
        with self.assertRaises(ValueError):
            test_addresses = [
                ipaddress.ip_network("192.168.1.65/29"),
                ipaddress.ip_network("10.0.1.248/32"),
            ]
        print("\nFinish testing that all fail due to no subnets.  All host bits\n")

    def test_02_fail_due_to_not_list(self):
        print("\nStart testing that all fail due to not a list passed\n")
        test_addresses = [
            ipaddress.ip_network("192.168.1.64/29"),
            ipaddress.ip_network("10.0.1.248/29"),
        ]
        for address in test_addresses:
            hosts_lists = []
            for x in address.hosts():
                hosts_lists.append(x)
            with self.assertRaises(TypeError):
                active_hosts = pinger(tuple(hosts_lists))
        print("\nFinish testing that all fail due to not a list passed\n")

    def test_03_fail_due_to_empy_list_arg(self):
        print("\nStart testing that all fail due to empty list passed\n")
        test_list = []
        with self.assertRaises(ValueError):
            pinger(test_list)
        print("\nFinish testing that all fail due to empty list passed\n")

    def test_04_pass_due_to_no_active_hosts(self):
        print("\nStart testing that passed due to no active hosts\n")
        test_addresses = [
            ipaddress.ip_network("192.168.1.0/29"),
            ipaddress.ip_network("10.0.1.16/29"),
        ]
        for address in test_addresses:
            hosts_lists = []
            for x in address.hosts():
                hosts_lists.append(x)
            with self.assertRaises(SystemExit):
                pinger(hosts_lists)
        print("\nFinish testing that all pass\n")

    def test_05_pass_due_to_no_arguments_passed(self):
        print("\nStart testing that all fail due to no arguments passed\n")
        with self.assertRaises(TypeError):
            pinger()
        print("\nFinish testing that all fail due to no arguments passed\n")

    def test_06_fail_due_to_no_not_an_IP(self):
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

    def test_07_pass_time_list_tuple(self):
        print("\nStart testing that pinger returns a tuple inside a dictionary\n")
        test_addresses = [
            ipaddress.ip_network("192.168.1.64/29"),
            ipaddress.ip_network("10.0.1.248/29"),
            ipaddress.ip_address("192.168.1.65"),
        ]
        for address in test_addresses:
            hosts_lists = []
            if isinstance(address, ipaddress.IPv4Network):
                for x in address.hosts():
                    hosts_lists.append(x)
            elif isinstance(address, ipaddress.IPv4Address):
                hosts_lists.append(address)
            active_hosts = pinger(hosts_lists)
            self.assertIsInstance(active_hosts, dict)
            for key in active_hosts.keys():
                self.assertIsInstance(active_hosts[key], dict)
                self.assertIsInstance(active_hosts[key]["ping"], tuple)
                self.assertEqual(len(active_hosts[key]["ping"]), 3)
            print(f"Tests passed for network {str(address)}")
        print("\nFinish testing that pinger returns a tuple inside a dictionary\n")


if __name__ == "__main__":
    unittest.main()