from typing import Type
import unittest
import ipaddress
import os
import sys
import json
from unittest.mock import patch

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)

from scan_mods.device_class import FoundDevice


class TestFoundDevice(unittest.TestCase):
    """
    Tests that the device class works for FoundDevice
    """

    test_ip01 = "192.168.1.65"
    test_ip02 = "192.168.1.65"
    test_ip03 = ipaddress.IPv4Address("192.168.1.65")
    test_ip04 = ipaddress.IPv4Address("192.168.1.68")
    test_time01 = (1.1, 1.35, 1.82)
    test_time02 = (1.1, 1.35, 1.82)
    test_ports01 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "Domain_Name": "test.local",
                "Server": "192.168.89.80",
                "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                "ns": "[ns 604800 IN A 192.168.89.80]",
                "www": "[www 604800 IN A 192.168.89.80]",
            },
            "80": {
                "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:42:50 GMT",
                "ETag": '"2ab2-5bc061fadc9e7-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3147",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "Name": "test.local.",
                "Record Type": "SOA",
                "Record Class": "IN",
                "nameserver": "192.168.89.80",
                "port": "53",
                "Answer": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "Canonical Name": "test.local.",
                "Minimum TTL": "604800",
                "CNAMES": [],
                "DNS Record Set": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "expiration": "1615900227.7461846",
            },
        },
    }
    test_closed_TCP_ports01 = {
        "20": {
            "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
        },
        "23": {
            "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
        },
    }
    test_closed_UDP_ports01 = {"43": {"ERROR": "Socket Timed Out"}}
    test_open_UDP_ports01 = {
        "53": {
            "Name": "test.local.",
            "Record Type": "SOA",
            "Record Class": "IN",
            "nameserver": "192.168.89.80",
            "port": "53",
            "Answer": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
            "Canonical Name": "test.local.",
            "Minimum TTL": "604800",
            "CNAMES": [],
            "DNS Record Set": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
            "expiration": "1615900227.7461846",
        },
    }
    test_open_TCP_ports01 = {
        "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
        "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
        "53": {
            "Domain_Name": "test.local",
            "Server": "192.168.89.80",
            "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
            "ns": "[ns 604800 IN A 192.168.89.80]",
            "www": "[www 604800 IN A 192.168.89.80]",
        },
        "80": {
            "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
            "Server": "Apache/2.4.41 (Ubuntu)",
            "Last-Modified": "Tue, 23 Feb 2021 19:42:50 GMT",
            "ETag": '"2ab2-5bc061fadc9e7-gzip"',
            "Accept-Ranges": "bytes",
            "Vary": "Accept-Encoding",
            "Content-Encoding": "gzip",
            "Content-Length": "3147",
            "Keep-Alive": "timeout=5, max=100",
            "Connection": "Keep-Alive",
            "Content-Type": "text/html",
        },
    }

    test_ports02 = {
        "TCP": {
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
        },
        "UDP": {
            "69": {"ERROR": "Socket Timed Out"},
        },
    }

    test_ports03 = {
        "TCP": {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "Domain_Name": "test.local",
                "Server": "192.168.89.80",
                "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                "ns": "[ns 604800 IN A 192.168.89.80]",
                "www": "[www 604800 IN A 192.168.89.80]",
            },
            "80": {
                "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:42:50 GMT",
                "ETag": '"2ab2-5bc061fadc9e7-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3147",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
        },
        "UDP": {
            "43": {"ERROR": "Socket Timed Out"},
            "53": {
                "Name": "test.local.",
                "Record Type": "SOA",
                "Record Class": "IN",
                "nameserver": "192.168.89.80",
                "port": "53",
                "Answer": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "Canonical Name": "test.local.",
                "Minimum TTL": "604800",
                "CNAMES": [],
                "DNS Record Set": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                "expiration": "1615900227.7461846",
            },
            "69": {"ERROR": "Socket Timed Out"},
        },
    }

    def test_001_class_init_pass(self):
        """
        Tests that a device can be created passing only the init variables
        """
        print("\nTest 001 - Start testing that class init works...")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertIsInstance(test_class, FoundDevice)
        self.assertIsInstance(test_class._IP, str)
        self.assertEqual(test_class._IP, self.test_ip01)
        self.assertIsInstance(test_class._response_time, tuple)
        self.assertEqual(test_class._response_time, self.test_time01)
        for test_item in [
            test_class._all_ports,
            test_class._username,
            test_class._password,
            test_class._enable_password,
            test_class._domain_name,
            test_class.device_info,
        ]:
            self.assertIsNone(test_item)

        for test_item in [
            test_class._open_tcp_ports,
            test_class._open_udp_ports,
            test_class._closed_tcp_ports,
            test_class._closed_udp_ports,
        ]:
            self.assertEqual(len(test_item), 0)
            self.assertIsInstance(test_item, dict)
            self.assertEqual(test_item, {})
        self.assertFalse(test_class._use_enable)

        test_class = FoundDevice(
            self.test_ip01,
            self.test_time01,
            "jmctsm",
            "ciscocisco",
            use_enable=True,
            enable_password="ciscocisco",
            domain_name="test.local",
        )
        self.assertIsInstance(test_class, FoundDevice)
        self.assertIsInstance(test_class._IP, str)
        self.assertEqual(test_class._IP, self.test_ip01)
        self.assertIsInstance(test_class._response_time, tuple)
        self.assertEqual(test_class._response_time, self.test_time01)
        for test_item in [
            test_class._all_ports,
            test_class.device_info,
        ]:
            self.assertIsNone(test_item)
        for test_item in [
            test_class._open_tcp_ports,
            test_class._open_udp_ports,
            test_class._closed_tcp_ports,
            test_class._closed_udp_ports,
        ]:
            self.assertEqual(len(test_item), 0)
            self.assertIsInstance(test_item, dict)
            self.assertEqual(test_item, {})
        self.assertEqual(test_class._username, "jmctsm")
        self.assertEqual(test_class._password, "ciscocisco")
        self.assertTrue(test_class._use_enable)
        self.assertEqual(test_class._enable_password, "ciscocisco")
        self.assertEqual(test_class._domain_name, "test.local")

        print("Test 001 - Finish testing that class init works\n")

    def test_002_init_raises_correct_errors(self):
        """
        Test that the init function raises the correct errors
        """
        print("\nTest 002 - Starting test that init raises the correct errors...")
        test_list = [
            (1, self.test_time01, TypeError),
            ("1", self.test_time01, ValueError),
            ("192.168.0.254", [1.1, 1.1, 1.1], TypeError),
            ("192.168.0.254", (1.1, 1.1), ValueError),
            ("192.168.0.254", [1.1, 1.1, "a"], TypeError),
        ]
        for test_tuple in test_list:
            with self.assertRaises(test_tuple[2]):
                test_class = FoundDevice(test_tuple[0], test_tuple[1])
        print("Test 002 - Finished test that init raises the correct errrors\n")

    def test_003_IP_getter_works(self):
        """
        Tests that the IP getter for the class is working
        """
        print("\nTest 003 - Start testing that class IP getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.IP, self.test_ip01)
        print("Test 003 - Finish testing that class IP getter works works\n")

    def test_004_set_IP_directly(self):
        """
        Tests that you cannot set the IP directly
        """
        print("\nTest 004 - Start testing that IP cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.IP = 4
        print(
            "Test 004 - Finish testing that response_time cannot be set be directly\n"
        )

    def test_005_response_time_getter_works(self):
        """
        Tests that the response time getter for the class is working
        """
        print("\nTest 005 - Start testing that class response time getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.response_time, self.test_time01)
        print("Test 005 - Finish testing that class response time getter works\n")

    def test_006_set_response_time_directly(self):
        """
        Tests that you cannot set the response_time directly
        """
        print("\nTest 006 - Start testing that response_time cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.response_time = 4
        print(
            "Test 006 - Finish testing that response_time cannot be set be directly\n"
        )

    def test_007_username_getter_works(self):
        """
        Tests that the username getter for the class is working
        """
        print("\nTest 007 - Start testing that class username getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.username, "Username has not been set yet")
        test_class._username = "jmctsm"
        self.assertEqual(test_class.username, "jmctsm")
        print("Test 007 - Finish testing that class username getter works\n")

    def test_008_username_directly(self):
        """
        Tests that you cannot set the username directly
        """
        print("\nTest 008 - Start testing that username cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.username = 4
        print("Test 008 - Finish testing that username cannot be set be directly\n")

    def test_009_password_getter_works(self):
        """
        Tests that the password getter for the class is working
        """
        print("\nTest 009 - Start testing that class password getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.password, "Password for device has not been given")
        test_class._password = "jmctsm"
        self.assertEqual(test_class.password, "Password for device has been given")
        print("Test 009 - Finish testing that class password getter works\n")

    def test_010_password_directly(self):
        """
        Tests that you cannot set the password directly
        """
        print("\nTest 010 - Start testing that password cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.password = 4
        print("Test 010 - Finish testing that password cannot be set be directly\n")

    def test_011_enable_password_getter_works(self):
        """
        Tests that the enable password getter for the class is working
        """
        print("\nTest 011 - Start testing that class enable password getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(
            test_class.enable_password, "Not using Enable password for this device"
        )
        test_class._use_enable = True
        self.assertEqual(
            test_class.enable_password, "Enable password for device has not been given"
        )
        test_class._enable_password = "jmctsm"
        self.assertEqual(
            test_class.enable_password, "Enable password for device has been given"
        )
        print("Test 009 - Finish testing that class enable password getter works\n")

    def test_012_enable_password_directly(self):
        """
        Tests that you cannot set the password directly
        """
        print(
            "\nTest 012 - Start testing that enable password cannot be set be directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.enable_password = 4
        print(
            "Test 012 - Finish testing that enable password cannot be set be directly\n"
        )

    def test_013_domain_name_getter_works(self):
        """
        Tests that the domain name getter for the class is working
        """
        print("\nTest 013 - Start testing that class domain name getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.domain_name, "Domain name has not been set yet")
        test_class._domain_name = "test.local"
        self.assertEqual(test_class.domain_name, "test.local")
        print("Test 013 - Finish testing that class domain name getter works\n")

    def test_014_domain_name_directly(self):
        """
        Tests that you cannot set the domain name directly
        """
        print("\nTest 014 - Start testing that domain name cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.domain_name = 4
        print("Test 014 - Finish testing that domain name cannot be set be directly\n")

    def test_015_all_ports_getter_works(self):
        """
        Tests that the all_ports getter for the class is working
        """
        print("\nTest 015 - Start testing that class ports getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertIsNone(test_class.all_ports)
        test_class._all_ports = {"a": {22: "Open"}}
        self.assertEqual(test_class.all_ports, {"a": {22: "Open"}})
        print("Test 015 - Finish testing that class ports getter works\n")

    def test_016_get_ports_works(self):
        """
        Tests that method get_ports works
        """
        print("\nTest 016 - Start testing that class get_ports works")
        with patch("scan_mods.device_class.port_scanner") as mock_port_scanner:
            mock_port_scanner.return_value = self.test_ports01
            test_class = FoundDevice(self.test_ip01, self.test_time01)
            test_class.get_ports()
            self.assertIsInstance(test_class.all_ports, dict)
            self.assertEqual(test_class.all_ports, self.test_ports01)
        print("Test 016 - Finish testing that class get_ports works\n")

    def test_017_all_ports_setter(self):
        """
        Tests that the all ports setter correctly functions
        """
        print("\nTest 017 - Start testing that class all_ports setter works")

        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_class.all_ports = {
            "TCP": {
                "20": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
                "23": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "53": {
                    "Domain_Name": "test.local",
                    "Server": "192.168.89.80",
                    "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                    "ns": "[ns 604800 IN A 192.168.89.80]",
                    "www": "[www 604800 IN A 192.168.89.80]",
                },
                "80": {
                    "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                    "Server": "Apache/2.4.41 (Ubuntu)",
                    "Last-Modified": "Tue, 23 Feb 2021 19:42:50 GMT",
                    "ETag": '"2ab2-5bc061fadc9e7-gzip"',
                    "Accept-Ranges": "bytes",
                    "Vary": "Accept-Encoding",
                    "Content-Encoding": "gzip",
                    "Content-Length": "3147",
                    "Keep-Alive": "timeout=5, max=100",
                    "Connection": "Keep-Alive",
                    "Content-Type": "text/html",
                },
            },
            "UDP": {
                "43": {"ERROR": "Socket Timed Out"},
                "53": {
                    "Name": "test.local.",
                    "Record Type": "SOA",
                    "Record Class": "IN",
                    "nameserver": "192.168.89.80",
                    "port": "53",
                    "Answer": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                    "Canonical Name": "test.local.",
                    "Minimum TTL": "604800",
                    "CNAMES": [],
                    "DNS Record Set": "test.local. 604800 IN SOA test.local. root.test.local. 2 604800 86400 2419200 604800",
                    "expiration": "1615900227.7461846",
                },
            },
        }
        self.assertEqual(test_class._all_ports, self.test_ports01)
        self.assertEqual(test_class._closed_tcp_ports, self.test_closed_TCP_ports01)
        self.assertEqual(test_class._closed_udp_ports, self.test_closed_UDP_ports01)
        self.assertEqual(test_class._open_tcp_ports, self.test_open_TCP_ports01)
        self.assertEqual(test_class._open_udp_ports, self.test_open_UDP_ports01)

        test_class.all_ports = self.test_ports02
        self.assertEqual(test_class._all_ports, self.test_ports03)
        print("Test 017 - Finish testing that class all_ports setter works\n")

    def test_018_all_ports_errors(self):
        """
        Tests that method get_ports produces correct errors
        """
        print("\nTest 018 - Start testing that class get_ports produces correct errors")
        with self.assertRaises(TypeError):
            test_class = FoundDevice(self.test_ip01, self.test_time01)
            test_class.all_ports = 1

        test_bad_port_list = [
            ({"1": {}}, KeyError),
            ({"TCP": 1}, TypeError),
        ]
        for test_tuple in test_bad_port_list:
            with self.assertRaises(test_tuple[1]):
                test_class = FoundDevice(self.test_ip01, self.test_time01)
                test_class.all_ports = test_tuple[0]

        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_class.all_ports = self.test_ports01
        test_bad_port_list = [
            ({"1": {}}, KeyError),
            ({"TCP": 1}, TypeError),
            ({"UDP": {"69": 1}}, TypeError),
        ]
        for test_tuple in test_bad_port_list:
            with self.assertRaises(test_tuple[1]):
                test_class = FoundDevice(self.test_ip01, self.test_time01)
                test_class.all_ports = test_tuple[0]

        print(
            "Test 018 - Finish testing that class all_ports produces correct errors\n"
        )

    def test_019_set_private_closed_open_ports(self):
        """
        Tests that set_private_closed_open_ports correctly passes
        """
        print(
            "\nTest 019 - Start testing that class set_private_closed_open_ports works"
        )

        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_class._all_ports = self.test_ports01

        self.assertEqual(test_class._all_ports, self.test_ports01)
        test_class.set_private_closed_open_ports()

        self.assertEqual(test_class._closed_tcp_ports, self.test_closed_TCP_ports01)
        self.assertEqual(test_class._closed_udp_ports, self.test_closed_UDP_ports01)
        self.assertEqual(test_class._open_tcp_ports, self.test_open_TCP_ports01)
        self.assertEqual(test_class._open_udp_ports, self.test_open_UDP_ports01)
        print(
            "Test 019 - Finish testing that class set_private_closed_open_ports works\n"
        )

    def test_020_all_ports_errors(self):
        """
        Tests that method set_private_closed_open_ports produces correct errors
        """
        print(
            "\nTest 020 - Start testing that class set_private_closed_open_ports produces correct errors"
        )
        test_bad_list = [
            ({"TCP": {"22": 1}}, TypeError),
            ({"UDP": {"22": 1}}, TypeError),
        ]
        for test_tuple in test_bad_list:
            with self.assertRaises(test_tuple[1]):
                test_class = FoundDevice(self.test_ip01, self.test_time01)
                test_class.set_private_closed_open_ports(test_tuple[0])
        print(
            "Test 020 - Finish testing that class set_private_closed_open_ports produces correct errors\n"
        )

    def test_021_open_tcp_ports_getter(self):
        """
        Tests that the open_tcp_ports getter for the class is working
        """
        print("\nTest 021 - Start testing that class open_tcp_ports getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.open_tcp_ports, {})
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class.open_tcp_ports, self.test_open_TCP_ports01)
        print("Test 021 - Finish testing that class open_tcp_ports getter works\n")

    def test_022_open_tcp_ports_directly(self):
        """
        Tests that you cannot set the open_tcp_ports directly
        """
        print(
            "\nTest 022 - Start testing that open_tcp_ports cannot be set be directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.open_tcp_ports = 4
        print(
            "Test 022 - Finish testing that open_tcp_ports cannot be set be directly\n"
        )

    def test_023_open_udp_ports_getter(self):
        """
        Tests that the open_udp_ports getter for the class is working
        """
        print("\nTest 023 - Start testing that class open_udp_ports getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.open_udp_ports, {})
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class.open_udp_ports, self.test_open_UDP_ports01)
        print("Test 023 - Finish testing that class open_udp_ports getter works\n")

    def test_024_open_udp_ports_directly(self):
        """
        Tests that you cannot set the open_udp_ports directly
        """
        print(
            "\nTest 024 - Start testing that open_udp_ports cannot be set be directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.open_udp_ports = 4
        print(
            "Test 024 - Finish testing that open_udp_ports cannot be set be directly\n"
        )

    def test_025_closed_tcp_ports_getter(self):
        """
        Tests that the closed_tcp_ports getter for the class is working
        """
        print("\nTest 025 - Start testing that class closed_tcp_ports getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.closed_tcp_ports, {})
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class.closed_tcp_ports, self.test_closed_TCP_ports01)
        print("Test 025 - Finish testing that class closed_tcp_ports getter works\n")

    def test_026_closed_tcp_ports_directly(self):
        """
        Tests that you cannot set the closed_tcp_ports directly
        """
        print(
            "\nTest 026 - Start testing that closed_tcp_ports cannot be set be directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.closed_tcp_ports = 4
        print(
            "Test 026 - Finish testing that closed_tcp_ports cannot be set be directly\n"
        )

    def test_027_closed_udp_ports_getter(self):
        """
        Tests that the closed_udp_ports getter for the class is working
        """
        print("\nTest 027 - Start testing that class closed_udp_ports getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.closed_udp_ports, {})
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class.closed_udp_ports, self.test_closed_UDP_ports01)
        print("Test 027 - Finish testing that class closed_udp_ports getter works\n")

    def test_028_closed_udp_ports_directly(self):
        """
        Tests that you cannot set the closed_udp_ports directly
        """
        print(
            "\nTest 028 - Start testing that closed_udp_ports cannot be set be directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.closed_udp_ports = 4
        print(
            "Test 028 - Finish testing that closed_udp_ports cannot be set be directly\n"
        )

    def test_029_class_hash_value(self):
        """
        Tests that you hash value returns the correct value
        """
        print("\nTest 029 - Start testing that the hash value returned is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(hash(test_class), hash(self.test_ip01))
        print("Test 029 - Finish testing that the hash value returned is correct\n")

    def test_030_class_bool_value(self):
        """
        Tests that you bool value returns the correct value
        """
        print("\nTest 030 - Start testing that the bool value returned is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertTrue(bool(test_class))
        print("Test 030 - Finish testing that the bool value returned is correct\n")

    def test_031_class_eq_method(self):
        """
        Tests that you class __eq__ method
        """
        print("\nTest 031 - Start testing that the __eq__ method...")
        test_class01 = FoundDevice(self.test_ip01, self.test_time01)
        self.assertTrue(test_class01 == self.test_ip01)
        test_class02 = FoundDevice(self.test_ip02, self.test_time02)
        self.assertTrue(test_class01 == test_class02)
        test_class01.all_ports = self.test_ports01
        test_class02.all_ports = self.test_ports01
        self.assertTrue(test_class01 == test_class02)
        self.assertTrue(test_class01 == self.test_ip03)

        # Now to test the False Ones
        self.assertFalse(test_class01 == "a")
        self.assertFalse(test_class01 == "192.168.1.66")
        test_class04 = FoundDevice("192.168.1.64", self.test_time01)
        test_class05 = FoundDevice("192.168.1.65", self.test_time01)
        self.assertFalse(test_class04 == test_class05)
        test_class06 = FoundDevice("192.168.1.67", self.test_time01)
        test_class07 = FoundDevice("192.168.1.67", (1.7, 1.7, 1.7))
        self.assertFalse(test_class06 == test_class07)
        self.assertFalse(test_class01 == test_class07)
        self.assertFalse(test_class01 == self.test_ip04)
        print("Test 031 - Finish testing that the __eq__ method\n")

    def test_032_device_info_grabber_method(self):
        """
        Test that the device_info_grabber method is called correctly
        """
        print(
            "\nTest 032 - Start testing that the device_info_grabber method can be called..."
        )
        with patch("scan_mods.device_class.port_scanner") as mock_port_scanner:
            mock_port_scanner.return_value = self.test_ports01
            with patch("scan_mods.device_class.device_grab") as mock_dev_info_grab:
                mock_dev_info_grab.return_value = {
                    "Worked": "Method called.  Tested in its own file"
                }
                test_class = FoundDevice(self.test_ip01, self.test_time01)
                test_class.get_ports()
                self.assertIsNone(test_class.device_info)
                test_class.device_info_grabber()
                self.assertIsInstance(test_class.device_info, dict)
                self.assertEqual(
                    test_class.device_info,
                    {"Worked": "Method called.  Tested in its own file"},
                )
        print(
            "Test 032 - Finish testing that the device_info_grabber method can be called\n"
        )

    def test_033_class_repr(self):
        """
        Tests that you class __repr__ method is correct
        """
        print("\nTest 033 - Start testing that the __repr__ method is correct...")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_string = f"{self.test_ip01} : "
        test_string += f"\n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms"
        test_string += f"\n\tusername is Username has not been set yet"
        test_string += f"\n\tpassword Password for device has not been given"
        test_string += f"\n\tenable password Not using Enable password for this device"
        test_string += f"\n\tdomain name is Domain name has not been set yet"
        self.assertEqual(repr(test_class), test_string)
        test_class.all_ports = self.test_ports01
        test_string += "\n\tOpen TCP Ports:"
        for key in self.test_open_TCP_ports01.keys():
            test_string += f"\n\t\t{key} : {self.test_open_TCP_ports01[key]}"
        test_string += "\n\tOpen UDP Ports:"
        for key in self.test_open_UDP_ports01.keys():
            test_string += f"\n\t\t{key} : {self.test_open_UDP_ports01[key]}"
        test_string += "\n\tClosed TCP Ports:"
        for key in self.test_closed_TCP_ports01.keys():
            test_string += f"\n\t\t{key} : {self.test_closed_TCP_ports01[key]}"
        test_string += "\n\tClosed UDP Ports:"
        for key in self.test_closed_UDP_ports01.keys():
            test_string += f"\n\t\t{key} : {self.test_closed_UDP_ports01[key]}"
        self.assertEqual(repr(test_class), test_string)
        print("Test 033 - Finish testing that the __repr__ method is correct\n")

    def test_034_class_str(self):
        """
        Tests that you class __str__ method is correct
        """
        print("\nTest 034 - Start testing that the __str__ method is correct...")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_string = f"{self.test_ip01} : "
        test_string += f"\n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms"
        test_string += f"\n\tusername is Username has not been set yet"
        test_string += f"\n\tpassword Password for device has not been given"
        test_string += f"\n\tenable password Not using Enable password for this device"
        test_string += f"\n\tdomain name is Domain name has not been set yet"
        self.assertEqual(str(test_class), test_string)
        test_class.all_ports = self.test_ports01
        test_string += "\n\tOpen TCP Ports:"
        for key in self.test_open_TCP_ports01.keys():
            test_string += f"\n\t\t{key} = {self.test_open_TCP_ports01[key]}"
        test_string += "\n\tOpen UDP Ports:"
        for key in self.test_open_UDP_ports01.keys():
            test_string += f"\n\t\t{key} = {self.test_open_UDP_ports01[key]}"
        test_string += "\n\tClosed TCP Ports:"
        for key in self.test_closed_TCP_ports01.keys():
            test_string += f"\n\t\t{key}"
        test_string += "\n\tClosed UDP Ports:"
        for key in self.test_closed_UDP_ports01.keys():
            test_string += f"\n\t\t{key}"
        self.assertEqual(str(test_class), test_string)
        print("Test 034 - Finish testing that the __str__ method is correct\n")

    def test_035_print_json_short(self):
        """
        Tests that the print_json_short function works correctly
        """
        print(
            "\nTest 035 - Start testing that the print_json_short function works correctly..."
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_dict = {
            self.test_ip01: {
                "ping_response_times": self.test_time01,
                "username": "Username has not been set yet",
                "password": "Password for device has not been given",
                "enable_password": "Not using Enable password for this device",
                "domain_name": "Domain name has not been set yet",
            }
        }
        self.assertEqual(test_class.print_json_short(), json.dumps(test_dict, indent=4))

        test_class.all_ports = self.test_ports01
        test_dict[self.test_ip01]["Open_TCP_Ports_List"] = list(
            self.test_open_TCP_ports01.keys()
        )
        test_dict[self.test_ip01]["Open_UDP_Ports_List"] = list(
            self.test_open_UDP_ports01.keys()
        )
        test_dict[self.test_ip01]["Closed_TCP_Ports_List"] = list(
            self.test_closed_TCP_ports01.keys()
        )
        test_dict[self.test_ip01]["Closed_UDP_Ports_List"] = list(
            self.test_closed_UDP_ports01.keys()
        )
        self.assertEqual(test_class.print_json_short(), json.dumps(test_dict, indent=4))

        with patch("scan_mods.device_class.port_scanner") as mock_port_scanner:
            mock_port_scanner.return_value = self.test_ports01
            with patch("scan_mods.device_class.device_grab") as mock_dev_info_grab:
                mock_dev_info_grab.return_value = {
                    "Version_Info": "Method called.  Tested in its own file"
                }
                test_class.device_info_grabber()
        test_dict[self.test_ip01][
            "Device_Info"
        ] = "Method called.  Tested in its own file"
        self.assertEqual(test_class.print_json_short(), json.dumps(test_dict, indent=4))

        print(
            "Test 035 - Finish testing that the print_json_short function works correctly\n"
        )

    def test_036_print_json_long(self):
        """
        Tests that the print_json_long function works correctly
        """
        print(
            "\nTest 036 - Start testing that the print_json_long function works correctly..."
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_dict = {
            self.test_ip01: {
                "ping_response_times": self.test_time01,
                "username": "Username has not been set yet",
                "password": "Password for device has not been given",
                "enable_password": "Not using Enable password for this device",
                "domain_name": "Domain name has not been set yet",
            }
        }
        self.assertEqual(test_class.print_json_long(), json.dumps(test_dict, indent=4))

        test_class.all_ports = self.test_ports01
        test_dict[self.test_ip01]["Open_TCP_Ports_List"] = self.test_open_TCP_ports01
        test_dict[self.test_ip01]["Open_UDP_Ports_List"] = self.test_open_UDP_ports01
        test_dict[self.test_ip01][
            "Closed_TCP_Ports_List"
        ] = self.test_closed_TCP_ports01
        test_dict[self.test_ip01][
            "Closed_UDP_Ports_List"
        ] = self.test_closed_UDP_ports01
        self.assertEqual(test_class.print_json_long(), json.dumps(test_dict, indent=4))

        with patch("scan_mods.device_class.port_scanner") as mock_port_scanner:
            mock_port_scanner.return_value = self.test_ports01
            with patch("scan_mods.device_class.device_grab") as mock_dev_info_grab:
                mock_dev_info_grab.return_value = {
                    "Version_Info": "Method called.  Tested in its own file"
                }
                test_class.device_info_grabber()
        test_dict[self.test_ip01]["Device_Info"] = {
            "Version_Info": "Method called.  Tested in its own file"
        }
        self.assertEqual(test_class.print_json_long(), json.dumps(test_dict, indent=4))

        print(
            "Test 036 - Finish testing that the print_json_long function works correctly\n"
        )


if __name__ == "__main__":
    unittest.main()
