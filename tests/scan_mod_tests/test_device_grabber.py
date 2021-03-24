from typing import Type
import unittest
import ipaddress
import os
import sys
import json

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

import scan_mods.device_grabber


class TestFoundDevice(unittest.TestCase):
    """
    Tests that the device grabber python file works as expected
    """

    good_ipv4_addresses = (
        ipaddress.ip_address("192.168.89.80"),
        ipaddress.ip_address("192.168.89.254"),
        "192.168.89.253",
        "192.168.1.65",
    )
    good_ports_port_checker = {
        "linux": {
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
        },
        "cisco": {
            "22": {"Return Information": "SSH-1.99-Cisco-1.25"},
        },
        "other_SSH": {
            "22": {"Return Information": "SSH"},
        },
        "other_port": {
            "222": {"Return Information": "SSH"},
        },
        "false_return": {
            "21": {"Return Information": "FTP"},
        },
    }
    good_usernames = [
        "jmctsm",
        "bob",
        "a",
    ]
    good_passwords = [
        "jmctsm",
        "bob",
        "a",
    ]

    def test_00_check_address_pass(self):
        """
        Tests that the check address function works as expected
        """
        print(
            "\nStarting the test that the check address function works as expected..."
        )
        for address in self.good_ipv4_addresses:
            result = scan_mods.device_grabber.check_address(address)
            self.assertIsInstance(result, str)
            self.assertEqual(result, str(address))
        print(
            "Finished the test that the check address function works as expected...\n"
        )

    def test_01_check_address_fail(self):
        """
        Tests that the check address function fails as expected
        """
        print(
            "\nStarting the test that the check address function fails as expected..."
        )
        bad_ipv4_addresses = (
            None,
            "1.1",
            1,
        )
        for address in bad_ipv4_addresses:
            if address is None:
                with self.assertRaises(ValueError):
                    scan_mods.device_grabber.check_address(address)
            if isinstance(address, str):
                with self.assertRaises(ipaddress.AddressValueError):
                    scan_mods.device_grabber.check_address(address)
            if isinstance(address, int):
                with self.assertRaises(TypeError):
                    scan_mods.device_grabber.check_address(address)
        print(
            "Finished the test that the check address function fails as expected...\n"
        )

    def test_02_check_ports_pass(self):
        """
        Tests that the check ports function works as expected
        """
        print("\nStarting the test that the check ports function works as expected...")
        for key, value in self.good_ports_port_checker.items():
            result = scan_mods.device_grabber.check_ports(value)
            self.assertIsInstance(result, tuple)
            if key == "linux":
                self.assertEqual(result, (22, "Linux"))
            if key == "cisco":
                self.assertEqual(result, (22, "Cisco"))
            if key == "other_SSH":
                self.assertEqual(result, (22, "Other"))
            if key == "other_port":
                self.assertEqual(result, (222, "Other"))
            if key == "false_return":
                self.assertEqual(result, (False, False))
        print("Finished the test that the check ports function works as expected...\n")

    def test_03_check_ports_fail(self):
        """
        Tests that the check ports function fails as expected
        """
        print("\nStarting the test that the check ports function fails as expected...")

        bad_ports_port_checker = {
            "not_dict": 22,
            "head_not_dict": {
                "22": ("Return Information", "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"),
            },
        }
        for key, value in bad_ports_port_checker.items():
            if key == "not_dict":
                with self.assertRaises(TypeError):
                    scan_mods.device_grabber.check_ports(value)
            if key == "head_not_dict":
                with self.assertRaises(TypeError):
                    scan_mods.device_grabber.check_ports(value)
        print("Finished the test that the check ports function fails as expected...\n")

    def test_04_check_username_pass(self):
        """
        Tests that the check username function works as expected
        """
        print(
            "\nStarting the test that the check username function works as expected..."
        )
        for username in self.good_usernames:
            name = scan_mods.device_grabber.check_username(username, "192.168.1.1")
            self.assertIsInstance(name, str)
            self.assertEquals(name, username)
        name = scan_mods.device_grabber.check_username(name=None, address="192.168.1.1")
        self.assertIsInstance(name, str)
        print(
            "Finished the test that the check username function works as expected...\n"
        )

    def test_05_check_password_pass(self):
        """
        Tests that the check password function works as expected
        """
        print(
            "\nStarting the test that the check password function works as expected..."
        )
        for password in self.good_passwords:
            name = scan_mods.device_grabber.check_password(password, "192.168.1.1")
            self.assertIsInstance(name, str)
            self.assertEquals(name, password)
        name = scan_mods.device_grabber.check_password(
            password=None, address="192.168.1.1"
        )
        self.assertIsInstance(password, str)
        print(
            "Finished the test that the check password function works as expected...\n"
        )

    def test_05_check_enable_password_pass(self):
        """
        Tests that the check enable password function works as expected
        """
        print(
            "\nStarting the test that the check enable password function works as expected..."
        )
        for password in self.good_passwords:
            name = scan_mods.device_grabber.check_enable_password(
                password, "192.168.1.1"
            )
            self.assertIsInstance(name, str)
            self.assertEquals(name, password)
        name = scan_mods.device_grabber.check_enable_password(
            password=None, address="192.168.1.1"
        )
        self.assertIsInstance(password, str)
        print(
            "Finished the test that the check password function works as expected...\n"
        )


if __name__ == "__main__":
    unittest.main()
