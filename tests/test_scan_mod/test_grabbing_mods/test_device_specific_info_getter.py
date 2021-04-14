from os.path import supports_unicode_filenames
import unittest
from unittest.mock import patch
import os
import sys
import netmiko
import netmiko.ssh_exception
import textfsm.parser

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

import scan_mods.grabbing_mods.device_specific_info_getter


class TestDeviceInfoGetter(unittest.TestCase):

    cisco_iosxe_no_en = {"192.168.89.254": "ios"}
    cisco_iosv_enable = {"192.168.89.253": "ios"}
    cisco_iosl2_no_enable = {"192.168.89.252": "ios"}
    cisco_iosxe_enable = {"192.168.89.247": "ios"}
    cisco_nx0s7 = {"192.168.89.251": "nxos_ssh"}
    linux_ubuntu_server = {"192.168.89.80": "linux"}

    username = "jmctsm"
    password = "ciscocisco"
    no_enable_password = None
    no_enable_device_list = [
        cisco_iosxe_no_en,
        cisco_iosl2_no_enable,
        cisco_nx0s7,
        linux_ubuntu_server,
    ]
    enable_device_list = [
        cisco_iosv_enable,
        cisco_iosxe_enable,
    ]

    enable_password = "ciscocisco"

    def test_01_all_pass(self):
        print("\nStarting test for all pass...")
        for device in self.no_enable_device_list:
            for device_ip, device_type in device.items():
                results = scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                    address=device_ip,
                    username=self.username,
                    password=self.password,
                    device_type=device_type,
                    enable_password_needed=False,
                )
                self.assertIsInstance(results, dict)
                self.assertGreaterEqual(len(results), 1)
        for device in self.enable_device_list:
            for device_ip, device_type in device.items():
                results = scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                    address=device_ip,
                    username=self.username,
                    password=self.password,
                    device_type=device_type,
                    enable_password_needed=True,
                    enable_password=self.enable_password,
                )
                self.assertIsInstance(results, dict)
                self.assertGreaterEqual(len(results), 1)
        print("Finished test for all pass\n")

    def test_02_check_device_type_pass(self):
        print("\nStarting test for check_device_type pass...")
        type_list = [
            ("ios", ("cisco_ios", "cisco_ios")),
            ("nxos_ssh", ("cisco_nxos_ssh", "cisco_nxos")),
            ("iosxr", ("cisco_xr", "cisco_xr")),
            ("linux", ("linux_ssh", "linux")),
        ]
        for test_tuple in type_list:
            type_of_device, correct_response = test_tuple
            result = (
                scan_mods.grabbing_mods.device_specific_info_getter.check_device_type(
                    type_of_device,
                    "192.168.0.254",
                )
            )
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], str)
            self.assertEqual(result, correct_response)
        print("Finished test for check_device_type pass\n")

    def test_03_check_device_type_raise_error(self):
        print("\nStarting test for check_device_type raises correct errors...")
        type_list = [
            (None, ValueError),
            ("nxo_ssh", ValueError),
            (1, TypeError),
        ]
        for test_tuple in type_list:
            type_input, correct_exception = test_tuple
            with self.assertRaises(correct_exception):
                scan_mods.grabbing_mods.device_specific_info_getter.check_device_type(
                    type_input,
                    "192.168.0.254",
                )
        print("Finished test for check_device_type raises correct errors\n")

    def test_04_find_commands_pass(self):
        print("\nStarting test for find_commands passes...")
        device_type_list = [
            "cisco_ios",
            "cisco_nxos",
            "cisco_xr",
            "linux",
        ]
        for device_type in device_type_list:
            results = scan_mods.grabbing_mods.device_specific_info_getter.find_commands(
                device_type
            )
            self.assertGreaterEqual(len(results), 1)
            self.assertIsInstance(results, dict)
            for key, value in results.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, str)
        print("Finished test for find_commands passes\n")

    def test_05_find_commands_raise_exceptions(self):
        print("\nStarting test for find_commands raises correct errors...")
        with self.assertRaises(TypeError):
            scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(1)
        print("Finished test for find_commands raises correct errors\n")

    def test_06_device_info_getter_raises_exceptions(self):
        print("\nStarting test for device_info_getter raises correct errors...")
        with self.assertRaises(ValueError):
            scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(None)

        test_list = [
            (
                netmiko.ssh_exception.NetmikoTimeoutException,
                {
                    "ERROR": {
                        "NetmikoTimeoutException": f"Device Connection Timed Out for 192.168.0.254",
                    }
                },
            ),
            (
                netmiko.ssh_exception.NetmikoAuthenticationException,
                {
                    "ERROR": {
                        "NetmikoAuthenticationException": f"Authentication failed for 192.168.0.254",
                    }
                },
            ),
        ]
        for test_tuple in test_list:
            test_exception, test_result = test_tuple
            with patch(
                "scan_mods.grabbing_mods.device_specific_info_getter.netmiko.ConnectHandler",
                side_effect=test_exception,
            ):
                result = scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                    address="192.168.0.254",
                    username="jmctsm",
                    password="ciscocisco",
                    device_type="ios",
                    enable_password_needed=False,
                )
                self.assertIsNotNone(result)
                self.assertGreaterEqual(len(result), 1)
                self.assertIsInstance(result, dict)
                self.assertDictEqual(result, test_result)

        with patch(
            "scan_mods.grabbing_mods.device_specific_info_getter.netmiko.ConnectHandler",
            side_effect=Exception,
        ):
            with self.assertRaises(Exception):
                scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                    address="192.168.0.254",
                    username="jmctsm",
                    password="ciscocisco",
                    device_type="ios",
                    enable_password_needed=False,
                )
        with patch(
            "scan_mods.grabbing_mods.device_specific_info_getter.find_commands",
            return_value={"show_ver": "show version"},
        ):
            with patch(
                "scan_mods.grabbing_mods.device_specific_info_getter.netmiko.ConnectHandler"
            ) as mock_ssh:
                # have to return the mock since that is the class returned to the
                # calling function.  Side Effect raises the exception to test for
                mock_ssh.return_value.send_command.side_effect = Exception
                with self.assertRaises(Exception):
                    scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                        address="192.168.0.254",
                        username="jmctsm",
                        password="ciscocisco",
                        device_type="ios",
                        enable_password_needed=False,
                    )

        test_list = [
            (
                textfsm.parser.TextFSMError,
                {},
            ),
            (
                OSError,
                {},
            ),
            (
                netmiko.ssh_exception.NetmikoTimeoutException,
                {"show_ver": "Timed-out reading channel, data not available."},
            ),
        ]
        for test_tuple in test_list:
            test_exception, test_output = test_tuple
            with patch(
                "scan_mods.grabbing_mods.device_specific_info_getter.find_commands",
                return_value={"show_ver": "show version"},
            ):
                with patch(
                    "scan_mods.grabbing_mods.device_specific_info_getter.netmiko.ConnectHandler"
                ) as mock_ssh:
                    # have to return the mock since that is the class returned to the
                    # calling function.  Side Effect raises the exception to test for
                    mock_ssh.return_value.send_command.side_effect = test_exception
                    result = scan_mods.grabbing_mods.device_specific_info_getter.device_info_getter(
                        address="192.168.0.254",
                        username="jmctsm",
                        password="ciscocisco",
                        device_type="ios",
                        enable_password_needed=False,
                    )
                    self.assertIsNotNone(result)
                    self.assertIsInstance(result, dict)
                    self.assertDictEqual(result, test_output)

        print("Finished test for device_info_getter raises correct errors\n")


if __name__ == "__main__":
    unittest.main()