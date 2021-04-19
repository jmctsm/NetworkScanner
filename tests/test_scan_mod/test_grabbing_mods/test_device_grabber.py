from typing import Type
import unittest
import ipaddress
import os
import sys
import json
from unittest import result
from unittest.mock import MagicMock, patch
import napalm
import paramiko
import paramiko.ssh_exception

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

import scan_mods.grabbing_mods.device_grabber


class TestFoundDevice(unittest.TestCase):
    """
    Tests that the device grabber python file works as expected
    """

    linux_testbox = "192.168.89.80"
    cisco_iosxe_no_en = "192.168.89.254"
    cisco_iosv_enable = "192.168.89.253"
    cisco_iosl2_no_enable = "192.168.89.252"
    cisco_nx0s7 = "192.168.89.251"
    cisco_iosxe_enable = "192.168.89.247"
    fake_testbox = "192.168.0.254"
    username = "jmctsm"
    password = "ciscocisco"
    enable_password = "ciscocisco"
    linux_ports = {
        "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
        "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
    }
    cisco_ports = {
        "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
        "22": {"Return Information": "SSH-1.99-Cisco-1.25"},
    }
    nexus_ports = {
        "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
        "22": {"Return Information": "SSH-2.0-OpenSSH_6.2 FIPS"},
    }
    fake_ports = {
        "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
    }
    no_enable_device_list = [
        (fake_testbox, fake_ports),
        (linux_testbox, linux_ports),
        (cisco_iosxe_no_en, cisco_ports),
        (cisco_iosl2_no_enable, cisco_ports),
        (cisco_nx0s7, nexus_ports),
    ]
    enable_device_list = [
        (cisco_iosv_enable, cisco_ports),
        (cisco_iosxe_enable, cisco_ports),
    ]

    test_get_device_type_list = [
        (linux_testbox, 22, username, password, None, "Linux", "linux"),
        (cisco_iosxe_no_en, 22, username, password, None, "Cisco", "ios"),
        (cisco_iosv_enable, 22, username, password, enable_password, "Cisco", "ios"),
        (cisco_iosl2_no_enable, 22, username, password, None, "Cisco", "ios"),
        (cisco_nx0s7, 22, username, password, None, "Other", "nxos_ssh"),
        (cisco_iosxe_enable, 22, username, password, enable_password, "Cisco", "ios"),
    ]

    test_get_config_napalm_list = [
        ("ios", cisco_iosxe_no_en, 22, username, password, None),
        ("ios", cisco_iosv_enable, 22, username, password, enable_password),
        ("ios", cisco_iosl2_no_enable, 22, username, password, None),
        ("nxos_ssh", cisco_nx0s7, 22, username, password, None),
        ("ios", cisco_iosxe_enable, 22, username, password, enable_password),
    ]

    def test_01_check_all_pass(self):
        print("\nTest 01 - Starting test to ensure that all pass...")
        for test_tuple in self.no_enable_device_list:
            device_ip, device_open_ports = test_tuple
            results = scan_mods.grabbing_mods.device_grabber.device_grab(
                address=device_ip,
                port_dict=device_open_ports,
                username=self.username,
                password=self.password,
                enable_password_needed=False,
            )
            self.assertIsInstance(results, dict)
            self.assertGreaterEqual(len(results), 1)
            for key in results.keys():
                self.assertTrue(key in ["Version_Info", "CONFIG"])

        for test_tuple in self.enable_device_list:
            device_ip, device_open_ports = test_tuple
            results = scan_mods.grabbing_mods.device_grabber.device_grab(
                address=device_ip,
                port_dict=device_open_ports,
                username=self.username,
                password=self.password,
                enable_password_needed=True,
                enable_password=self.enable_password,
            )
            self.assertIsInstance(results, dict)
            self.assertGreaterEqual(len(results), 1)
            for key in results.keys():
                self.assertTrue(key in ["Version_Info", "CONFIG"])
        print("Test 01 - Finish test that all pass")

    def test_02_check_ports_pass(self):
        """
        Tests that the check ports function works as expected
        """
        print(
            "\nTest 02 - Starting the test that the check ports function works as expected..."
        )
        test_list = [
            (self.linux_ports, (22, "Linux")),
            (self.cisco_ports, (22, "Cisco")),
            (self.nexus_ports, (22, "Other")),
            (self.fake_ports, (False, False)),
            (
                {
                    "2222": {
                        "Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"
                    }
                },
                (2222, "Other"),
            ),
        ]

        for test_tuple in test_list:
            test_ports, correct_value = test_tuple
            results = scan_mods.grabbing_mods.device_grabber.check_ports(test_ports)
            self.assertIsInstance(results, tuple)
            self.assertEqual(len(results), 2)
            self.assertEqual(results, correct_value)

        print(
            "Test 02 - Finished the test that the check ports function works as expected...\n"
        )

    def test_03_check_ports_fail(self):
        """
        Tests that the check ports function fails as expected
        """
        print(
            "\nTest 03 - Starting the test that the check ports function fails as expected..."
        )
        with self.assertRaises(TypeError):
            scan_mods.grabbing_mods.device_grabber.check_address(22)

        # This does not seem to be working for raising an exception
        with patch("builtins.str") as mock_str:
            mock_str.side_effect = Exception
            with self.assertRaises(Exception):
                scan_mods.grabbing_mods.device_grabber.check_address(22)

        with self.assertRaises(TypeError):
            scan_mods.grabbing_mods.device_grabber.check_address({"2222": {22}})

        print(
            "Test 03 - Finished the test that the check ports function fails as expected...\n"
        )

    def test_04_get_device_type_pass(self):
        """
        Tests that the get_device_type passes correctly
        """
        print(
            "\nTest 04 - Starting the test that get_device_type function works as expected..."
        )

        for test_tuple in self.test_get_device_type_list:
            results = scan_mods.grabbing_mods.device_grabber.get_device_type(
                test_tuple[0],
                test_tuple[1],
                test_tuple[2],
                test_tuple[3],
                test_tuple[4],
                test_tuple[5],
            )
            self.assertIsNotNone(results)
            self.assertIsInstance(results, dict)
            self.assertGreaterEqual(len(results), 1)
            self.assertEqual(results["OS Type"], test_tuple[6])

        print(
            "Test 04 - Finished the test that get_device_type function works as expected...\n"
        )

    def test_05_get_device_type_fail(self):
        """
        Tests that the get_device_type fails correctly
        """
        print(
            "\nTest 05 - Starting the test that get_device_type function fails as expected..."
        )
        test_fail_get_device_type_list = [
            (1, 22, self.username, self.password, None, "Linux", "linux"),
            (self.linux_testbox, 22, 1, self.password, None, "Linux", "linux"),
            (self.linux_testbox, 22, self.username, 1, None, "Linux", "linux"),
            (self.linux_testbox, 22, self.username, self.password, None, 1, "linux"),
        ]
        for test_tuple in test_fail_get_device_type_list:
            # Raise an error if these things are not a string
            with self.assertRaises(TypeError):
                scan_mods.grabbing_mods.device_grabber.get_device_type(
                    test_tuple[0],
                    test_tuple[1],
                    test_tuple[2],
                    test_tuple[3],
                    test_tuple[4],
                    test_tuple[5],
                )

        # error is IP address is not a true IP address
        with self.assertRaises(ipaddress.AddressValueError):
            scan_mods.grabbing_mods.device_grabber.get_device_type(
                "a",
                22,
                self.username,
                self.password,
                None,
                "Linux",
            )

        # raise an error is the port is not an int
        with self.assertRaises(TypeError):
            scan_mods.grabbing_mods.device_grabber.get_device_type(
                self.linux_testbox,
                "a",
                self.username,
                self.password,
                None,
                "Linux",
            )

        # raise an error if the port is too low or too high
        for test_num in [-1, 1_000_000]:
            with self.assertRaises(ValueError):
                scan_mods.grabbing_mods.device_grabber.get_device_type(
                    self.linux_testbox,
                    test_num,
                    self.username,
                    self.password,
                    None,
                    "Linux",
                )

        # raise an error if the enable password is not a string
        with self.assertRaises(TypeError):
            scan_mods.grabbing_mods.device_grabber.get_device_type(
                self.linux_testbox,
                60_000,
                self.username,
                self.password,
                1,
                "Linux",
            )

        test_list = ["Cisco", "Linux", "Other"]
        for test_header in test_list:
            with patch(
                "scan_mods.grabbing_mods.device_grabber.paramiko.SSHClient"
            ) as mock_ssh_client:
                stderr = MagicMock()
                stderr.readlines().return_value = "file1\nfile2\nfile3\n"
                with self.assertRaises(ValueError):
                    scan_mods.grabbing_mods.device_grabber.get_device_type(
                        self.linux_testbox,
                        22,
                        self.username,
                        self.password,
                        None,
                        test_header,
                    )

        print(
            "Test 05 - Finished the test that get_device_type function fails as expected\n"
        )

    def test_06_get_device_type_error_returns(self):
        """
        Tests that the get_device_type returns upon certain errors
        """
        print(
            "\nTest 06 - Starting the test that get_device_type function returns as expected for certain errors..."
        )

        # cannot test for paramiko.ssh_exception.NoValidConnectionsError because it wraps multiple other
        # errors.
        test_list = [
            (
                paramiko.AuthenticationException,
                {
                    "Version Info": "[ERROR] paramiko.AuthenticationException: Authentication failed for device 192.168.89.80"
                },
            ),
            (
                TimeoutError,
                {
                    "Version Info": "[ERROR] TimeoutError: Connection timed out for device 192.168.89.80"
                },
            ),
        ]
        for test_tuple in test_list:
            with patch(
                "scan_mods.grabbing_mods.device_grabber.paramiko.SSHClient"
            ) as mock_ssh_client:
                mock_ssh_client.return_value.connect.side_effect = test_tuple[0]
                result = scan_mods.grabbing_mods.device_grabber.get_device_type(
                    self.linux_testbox,
                    22,
                    self.username,
                    self.password,
                    None,
                    "Linux",
                )
                self.assertIsInstance(result, dict)
                self.assertEqual(result, test_tuple[1])

        print(
            "Test 06 - Finished the test that get_device_type function returns as expected for certain errors\n"
        )

    def test_07_get_config_napalm_pass(self):
        """
        Tests that the get_config_napalm passes
        """
        print(
            "\nTest 07 - Starting the test that get_config_napalm function passes correctly..."
        )
        for test_tuple in self.test_get_config_napalm_list:
            results = scan_mods.grabbing_mods.device_grabber.get_config_napalm(
                dev_driver=test_tuple[0],
                host=test_tuple[1],
                port=test_tuple[2],
                usern=test_tuple[3],
                passw=test_tuple[4],
                enable_password=test_tuple[5],
            )
            self.assertIsInstance(results, dict)
            self.assertGreaterEqual(len(results), 1)
            for key in results.keys():
                self.assertIn(
                    key,
                    [
                        "Device_Facts",
                        "Device_Optics",
                        "Device_Network_Instances",
                        "Device_LLDP_Detail",
                        "Device_LLDP",
                        "Device_Environment",
                        "Device_Interfaces",
                        "Device_Interfaces_IP",
                        "Device_SNMP_Information",
                        "Device_Users",
                        "Device_Startup_Config_File_Location",
                        "Device_Running_Config_File_Location",
                        "Device_Candidate_Config_File_Location",
                        "Device_Startup_Config_Full_File_Location",
                        "Device_Running_Config_Full_File_Location",
                        "Device_Candidate_Config_Full_File_Location",
                    ],
                )
        print(
            "Test 07 - Finished the test that get_config_napalm function passes correctly\n"
        )

    def test_08_get_config_napalm_raise_errors(self):
        """
        Test that get_config_napalm raises the correct errors
        """
        print(
            "\nTest 08 - Starting the test that get_config_napalm raises the correct errors..."
        )

        # Tests that initial type checkers work correctly
        bad_test_list = [
            (1, "a", 1, "a", "a", None, TypeError),
            ("a", 1, 1, "a", "a", None, TypeError),
            ("a", "a", 1, 1, "a", None, TypeError),
            ("a", "a", 1, "a", 1, None, TypeError),
            ("a", "a", "a", "a", "a", None, TypeError),
            ("a", "192.168.0.254", 1, "a", "a", 1, TypeError),
            ("a", "a", 1, "a", "a", "a", ipaddress.AddressValueError),
            ("a", "192.168.0.254", 1, "a", "a", "a", ValueError),
            ("ios", "192.168.0.254", 1_000_000, "a", "a", "a", ValueError),
            ("ios", "192.168.0.254", -1, "a", "a", "a", ValueError),
        ]
        for test_tuple in bad_test_list:
            with self.assertRaises(test_tuple[6]):
                scan_mods.grabbing_mods.device_grabber.get_config_napalm(
                    dev_driver=test_tuple[0],
                    host=test_tuple[1],
                    port=test_tuple[2],
                    usern=test_tuple[3],
                    passw=test_tuple[4],
                    enable_password=test_tuple[5],
                )

        with patch(
            "scan_mods.grabbing_mods.device_grabber.napalm.get_network_driver"
        ) as mock_driver:
            mock_driver.return_value.side_effect = ValueError
            result = scan_mods.grabbing_mods.device_grabber.get_config_napalm(
                "ios",
                "192.168.89.254",
                22,
                "jmctsm",
                "ciscocisco",
            )
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 0)
        print(
            "Test 08 - Finished the test that get_config_napalm raises the correct errors\n"
        )

    def test_09_directory_checker_pass(self):
        """
        Tests that the directory_checker passes
        """
        print(
            "\nTest 09 - Starting the test that directory_checker function passes correctly..."
        )
        test_addresses = [None, 1]
        with self.assertRaises(ValueError):
            scan_mods.grabbing_mods.device_grabber.directory_checker(None)

        with patch("scan_mods.grabbing_mods.device_grabber.os") as mock_os:
            mock_os.getcwd.return_value = "/root/test/"
            mock_os.listdir.return_value = ["Output"]
            mock_os.path.exists.retur_value = True
            result = scan_mods.grabbing_mods.device_grabber.directory_checker(
                "192.168.0.254"
            )
            self.assertIsInstance(result, str)
            self.assertEqual(result, "/root/test//Output/Scans/192.168.0.254")

        with patch("scan_mods.grabbing_mods.device_grabber.os") as mock_os:
            mock_os.getcwd.return_value = "/root/Output/test1/test2/test3/test"
            mock_os.listdir.side_effect = ["test", "test3", "test2", "test1", "Output"]
            mock_os.path.exists.retur_value = True
            result = scan_mods.grabbing_mods.device_grabber.directory_checker(
                "192.168.0.254"
            )
            self.assertIsInstance(result, str)
            self.assertEqual(result, "../../../..//Output/Scans/192.168.0.254")

        print(
            "Test 09 - Finished the test that directory_checker function passes correctly\n"
        )

    def test_10_device_grab_fails_correctly(self):
        """
        Tests that the device_grab function fails correctly
        """
        print(
            "\nTest 10 - Starting the test that device_grab raises the correct errors..."
        )
        with patch(
            "scan_mods.grabbing_mods.device_grabber.check_ports"
        ) as mock_check_ports:
            mock_check_ports.return_value = (False, False)
            result = scan_mods.grabbing_mods.device_grabber.device_grab(
                "192.168.0.1",
                self.linux_ports,
                "jmctsm",
                "ciscocisco",
            )
            self.assertIsInstance(result, dict)
            self.assertEqual(
                result,
                {
                    "Version_Info": ["No Version information was available"],
                    "CONFIG": {
                        "Open_Close": False,
                        "Open_Close_Msg": "SSH is not open on the device for ports scanned",
                        "Device_Information": {},
                    },
                },
            )

        with self.assertRaises(ValueError):
            scan_mods.grabbing_mods.device_grabber.device_grab(
                "192.168.0.1",
                self.linux_ports,
                "jmctsm",
                "ciscocisco",
                enable_password_needed="a",
            )

        with patch(
            "scan_mods.grabbing_mods.device_grabber.check_ports"
        ) as mock_check_ports:
            mock_check_ports.return_value = (22, "Cisco")
            with patch(
                "scan_mods.grabbing_mods.device_grabber.get_device_type"
            ) as mock_get_device_type:
                mock_get_device_type.return_value = {
                    "Version Info": "[ERROR] Error_TEST"
                }
                result = scan_mods.grabbing_mods.device_grabber.device_grab(
                    "192.168.0.1",
                    self.linux_ports,
                    "jmctsm",
                    "ciscocisco",
                )
                self.assertIsInstance(result, dict)
                self.assertEqual(
                    result,
                    {"Version_Info": "[ERROR] Error_TEST"},
                )

        print(
            "Test 10 - Finished the test that device_grab raises the correct errors\n"
        )


if __name__ == "__main__":
    unittest.main()
