import unittest
import ipaddress
import os
import sys
from unittest.mock import patch

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


import scan_mods.mp_pinger


class TestPinger(unittest.TestCase):
    """
    Tests that pinger works
    """

    mp_test_addresses = [
        "192.168.0.8/29",
        "192.168.89.0/24",
        "192.168.0.254",
    ]

    mp_test_networks = ["192.168.0.8/29", "192.168.89.0/24", "192.168.0.128/25"]

    sp_test_addresses = [
        "192.168.0.192/26",
    ]

    def unpack_addresses(self, addresses_to_test):
        """
        function to unpack addresses for all test functions
        Args:
            addresses_to_test (list) : address list of addresses or networks to test
        return:
             (list) : list of the individual addresses to run against
        """
        if len(addresses_to_test) == 0:
            raise ValueError(
                "There were no arguments passed to the function.  That is wrong.  Closing"
            )

        return_addresses = []
        for address in addresses_to_test:
            if "/" in address:
                try:
                    six_or_four = ipaddress.ip_network(address)
                except ValueError:
                    print(f"{address} is not a valid subnet.  Skipping.")
                    continue
                for address_host in six_or_four.hosts():
                    return_addresses.append(str(address_host))
            else:
                try:
                    ipaddress.ip_address(address)
                except ValueError:
                    print(f"{address} is not a valid address.  Skipping.")
                    continue
                return_addresses.append(str(address))
        for address in return_addresses:
            try:
                ipaddress.ip_address(address)
            except ValueError:
                raise ValueError(f"{address} is not an IPv4/v6 address. Shutting Down")
        if len(return_addresses) > 0:
            return return_addresses
        else:
            raise ValueError("No usable addresses to scan")

    def test_01_all_pass_pinger(self):
        print("\nStart testing that all pass and return time values")
        hosts_lists = self.unpack_addresses(self.mp_test_addresses)
        active_hosts = scan_mods.mp_pinger.pinger(hosts_lists)
        self.assertGreaterEqual(len(active_hosts), 0)
        self.assertIsInstance(active_hosts, dict)
        for key in active_hosts.keys():
            self.assertIn(key, hosts_lists)
            self.assertIsInstance(active_hosts[key], dict)
            self.assertIsInstance(active_hosts[key]["ping_response_time"], tuple)
            self.assertEqual(len(active_hosts[key]["ping_response_time"]), 3)
        print("Finish testing that all pass\n")

    def test_02_all_pass_ping_address(self):
        print("\nStart testing that all pass for ping_address")
        hosts_lists = self.unpack_addresses(self.sp_test_addresses)
        for host in hosts_lists:
            return_value = scan_mods.mp_pinger.ping_address(host)
            self.assertTrue(
                isinstance(return_value, tuple) or isinstance(return_value, str)
            )
            if isinstance(return_value, str):
                self.assertEqual(return_value, "TIMEOUT")
            if isinstance(return_value, tuple):
                self.assertIsInstance(return_value[0], str)
                self.assertEqual(return_value[0], host)
                self.assertIsInstance(return_value[1], tuple)
                self.assertEqual(len(return_value[1]), 3)
                self.assertIsInstance(return_value[1][0], float)
                self.assertIsInstance(return_value[1][1], float)
                self.assertIsInstance(return_value[1][2], float)
        print("Finish testing that all pass\n")

    def test_03_pinger_fail_as_expected(self):
        print("\nStart testing that all fail due to empty list passed")
        test_list = []
        with self.assertRaises(ValueError):
            scan_mods.mp_pinger.pinger(test_list)
        print("Finish testing that all fail due to empty list passed\n")
        print("\nStart testing that all fail due to not a list passed")
        test_list = [(1, 1), "a", 1.1]
        for entry in test_list:
            with self.assertRaises(TypeError):
                scan_mods.mp_pinger.pinger(tuple(entry))
        print("Finish testing that all fail due to not a list passed\n")
        print("\nStart testing that all fail due to no subnets.  All host bits")
        with self.assertRaises(ValueError):
            test_02_addresses = [
                ipaddress.ip_network("192.168.1.65/29"),
                ipaddress.ip_network("10.0.1.248/32"),
            ]
            for address in test_02_addresses:
                scan_mods.mp_pinger.pinger(address)
        print("Finish testing that all fail due to no subnets.  All host bits\n")

    def test_04_pass_due_to_no_active_hosts(self):
        print("\nStart testing that passed due to no active hosts")
        no_active_hosts_list = [
            "192.168.1.0/29",
            "10.0.1.16/29",
        ]
        hosts_lists = self.unpack_addresses(no_active_hosts_list)
        with self.assertRaises(Exception):
            scan_mods.mp_pinger.pinger(hosts_lists)
        print("Finish testing that passed due to no active hosts\n")

    def test_05_pass_due_to_no_arguments_passed_to_pinger(self):
        print("\nStart testing that all fail due to no arguments passed\n")
        with self.assertRaises(TypeError):
            scan_mods.mp_pinger.pinger()
        print("\nFinish testing that all fail due to no arguments passed\n")

    def test_06_fail_due_to_no_not_an_IP_to_pinger(self):
        print("\nStart testing that pinger fails due to an IP not being in the list\n")
        test_addresses = [
            "10.0.1.254",
            "192.168.1.65",
            "abc",
            123,
        ]
        with self.assertRaises(ValueError):
            scan_mods.mp_pinger.pinger(test_addresses)
        print("\nFinish testing that pinger fails due to an IP not being in the list\n")

    def test_07_fail_due_to_no_not_an_IP_to_ping_address(self):
        print("\nStart testing that pinger fails due to an IP not being in the list\n")
        test_addresses = [
            "10.0.1.254",
            "10.0.1.16/29",
            "abc",
            123,
        ]
        with self.assertRaises(ValueError):
            for address in test_addresses:
                scan_mods.mp_pinger.ping_address(address)
        print("\nFinish testing that pinger fails due to an IP not being in the list\n")


if __name__ == "__main__":
    unittest.main()