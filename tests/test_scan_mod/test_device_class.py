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

from scan_mods.device_class import FoundDevice


class TestFoundDevice(unittest.TestCase):
    """
    Tests that the device class works for FoundDevice
    """

    test_ip01 = ipaddress.IPv4Address("192.168.1.65")
    test_time01 = (1.1, 1.35, 1.82)
    test_ip02 = ipaddress.IPv4Address("192.168.1.65")
    test_time02 = (1.82, 1.35, 1.1)
    test_ip03 = "192.168.1.65"
    test_ip04 = ipaddress.IPv4Address("192.168.1.66")
    test_time04 = (1.1, 1.35, 1.82)
    test_ip05 = "192.168.89.80"
    test_ip06 = "1.1.1"
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
            "25": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "37": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "43": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "53": {
                "Domain_Name": "test.local",
                "Server": "192.168.89.80",
                "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                "ns": "[ns 604800 IN A 192.168.89.80]",
                "www": "[www 604800 IN A 192.168.89.80]",
            },
            "79": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
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
            "88": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "109": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "110": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "115": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "118": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "143": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "162": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "179": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "194": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "443": {
                "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:43:27 GMT",
                "ETag": '"2ab0-5bc0621d8c961-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3145",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
            "464": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "465": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "515": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "530": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "543": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "544": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "547": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "993": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "995": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "1080": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3128": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3306": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "3389": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5432": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5900": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "5938": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "8080": {
                "Date": "Tue, 09 Mar 2021 13:09:45 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Tue, 23 Feb 2021 19:51:02 GMT",
                "ETag": '"2abf-5bc063cf93aac-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3157",
                "Keep-Alive": "timeout=5, max=100",
                "Connection": "Keep-Alive",
                "Content-Type": "text/html",
            },
            "8443": {
                "Date": "Tue, 09 Mar 2021 13:09:44 GMT",
                "Server": "Apache/2.4.41 (Ubuntu)",
                "Last-Modified": "Mon, 08 Mar 2021 18:24:30 GMT",
                "ETag": '"2abf-5bd0a8b7734dc-gzip"',
                "Accept-Ranges": "bytes",
                "Vary": "Accept-Encoding",
                "Content-Encoding": "gzip",
                "Content-Length": "3159",
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
            "67": {"ERROR": "Socket Timed Out"},
            "69": {"ERROR": "Socket Timed Out"},
            "88": {"ERROR": "Socket Timed Out"},
            "118": {"ERROR": "Socket Timed Out"},
            "123": {"ERROR": "Socket Timed Out"},
            "161": {"ERROR": "Socket Timed Out"},
            "162": {"ERROR": "Socket Timed Out"},
            "194": {"ERROR": "Socket Timed Out"},
            "464": {"ERROR": "Socket Timed Out"},
            "514": {"ERROR": "Socket Timed Out"},
            "530": {"ERROR": "Socket Timed Out"},
            "547": {"ERROR": "Socket Timed Out"},
            "995": {"ERROR": "Socket Timed Out"},
            "1080": {"ERROR": "Socket Timed Out"},
            "3389": {"ERROR": "Socket Timed Out"},
            "5938": {"ERROR": "Socket Timed Out"},
            "8080": {"ERROR": "Socket Timed Out"},
            "8443": {"ERROR": "Socket Timed Out"},
        },
    }

    def test_000_class_init_pass(self):
        """
        Tests that a device can be created passing only the init variables
        """
        print("\nStart testing that class init works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertIsInstance(test_class, FoundDevice)
        self.assertIsInstance(test_class._IP, ipaddress.IPv4Address)
        self.assertEqual(test_class._IP, self.test_ip01)
        self.assertIsInstance(test_class._response_time, tuple)
        self.assertEqual(test_class._response_time, self.test_time01)
        self.assertIsNone(test_class._all_ports)
        self.assertEqual(len(test_class._open_tcp_ports), 0)
        self.assertIsInstance(test_class._open_tcp_ports, dict)
        self.assertEqual(len(test_class._open_udp_ports), 0)
        self.assertIsInstance(test_class._open_udp_ports, dict)
        self.assertEqual(len(test_class._closed_tcp_ports), 0)
        self.assertIsInstance(test_class._closed_tcp_ports, dict)
        self.assertEqual(len(test_class._closed_udp_ports), 0)
        self.assertIsInstance(test_class._closed_udp_ports, dict)
        print("Finish testing that class init works\n")

    def test_001_IP_getter_works(self):
        """
        Tests that the IP getter for the class is working
        """
        print("\nStart testing that class IP getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.IP, self.test_ip01)
        print("Finish testing that class IP getter works works\n")

    def test_002_response_time_getter_works(self):
        """
        Tests that the response time getter for the class is working
        """
        print("\nStart testing that class response time getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(test_class.response_time, self.test_time01)
        print("Finish testing that class response time getter works\n")

    def test_003_initialize_with_no_arguments(self):
        """
        Test to see what if can initialize the class with no arguments
        """
        print("\nStart testing that class init fails with no variables")
        with self.assertRaises(TypeError):
            test_class = FoundDevice()
        print("Finish testing that class init works\n")

    def test_004_response_time_not_tuple(self):
        """
        Tests that a device creation fails for response time not being a tuple
        """
        print("\nStart testing response time not a tuple")
        test_time = [1.1, 1.35, 1.82]
        with self.assertRaises(TypeError):
            FoundDevice(self.test_ip01, test_time)
        print("Finish testing response time not a tuple\n")

    def test_005_IP_Address_wrong_object(self):
        """
        Tests that a device creation fails for the IP not being an IPv4 Address object
        """
        print("\nStart testing address not being an IPv4 Address object")
        test_ip = "192.168.1.65"
        with self.assertRaises(TypeError):
            test_class = FoundDevice(test_ip, self.test_time01)
        print("Finish testing address not being an IPv4 Address object\n")

    def test_006_set_response_time_directly(self):
        """
        Tests that you cannot set the response_time directly
        """
        print("\nStart testing that response_time cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.response_time = 4
        print("Finish testing that response_time cannot be set be directly\n")

    def test_007_set_IP_directly(self):
        """
        Tests that you cannot set the IP directly
        """
        print("\nStart testing that IP cannot be set be directly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        with self.assertRaises(AttributeError):
            test_class.IP = 4
        print("Finish testing that response_time cannot be set be directly\n")

    def test_008_class_hash_value(self):
        """
        Tests that you hash value returns the correct value
        """
        print("\nStart testing that the hash value returned is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(hash(test_class), hash(self.test_ip01))
        print("Finish testing that the hash value returned is correct\n")

    def test_009_class_bool_value(self):
        """
        Tests that you bool value returns the correct value
        """
        print("\nStart testing that the bool value returned is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertTrue(bool(test_class))
        print("Finish testing that the bool value returned is correct\n")

    def test_010_class_eq_value_true(self):
        """
        Tests that you class __eq__ method returns True
        """
        print("\nStart testing that the __eq__ method returns True")
        test_class01 = FoundDevice(self.test_ip01, self.test_time01)
        test_class02 = FoundDevice(self.test_ip02, self.test_time02)
        self.assertTrue(test_class01 == test_class02)
        self.assertTrue(test_class01 == self.test_ip02)
        self.assertTrue(test_class01 == self.test_ip03)
        print("Finish testing that the __eq__ method returns True\n")

    def test_011_class_eq_value_false(self):
        """
        Tests that you class __eq__ method returns False
        """
        print("\nStart testing that the __eq__ method returns False")
        test_class01 = FoundDevice(self.test_ip01, self.test_time01)
        test_class02 = FoundDevice(self.test_ip04, self.test_time04)
        self.assertFalse(test_class01 == test_class02)
        self.assertFalse(test_class01 == self.test_ip04)
        self.assertFalse(test_class01 == self.test_ip05)
        self.assertFalse(test_class01 == self.test_ip06)
        print("Finish testing that the __eq__ method returns False\n")

    def test_012_class_repr(self):
        """
        Tests that you class __repr__ method is correct
        """
        print("\nStart testing that the __repr__ method is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(
            repr(test_class),
            f"{self.test_ip01} : \n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms",
        )
        test_class.all_ports = self.test_ports01
        self.assertRegex(
            repr(test_class),
            f"{self.test_ip01} : \n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms\n\tOpen TCP Ports:.*",
        )
        print("Finish testing that the __repr__ method is correct\n")

    def test_013_class_init_response_time_short(self):
        """
        Tests that a device creation fails if the tuple for response time is not length of 3
        """
        print(
            "\nStart testing that class init fails with response time is less than length of 3"
        )
        test_time_01 = (1.1, 1.35)
        with self.assertRaises(ValueError):
            FoundDevice(self.test_ip01, test_time_01)
        test_time_02 = (1.1, 1.35, 1.56, 1.78, 1.96)
        with self.assertRaises(ValueError):
            FoundDevice(self.test_ip01, test_time_02)
        print(
            "Finish testing that class init fails with response time is less than length of 3\n"
        )

    def test_014_testing_port_setter_empty(self):
        """
        Tests that the port setter works with an empty port list in the class
        """
        print("\nStart testing port setter works with an empty port list in the class")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class._all_ports, self.test_ports01)
        print("Finish testing port setter works with an empty port list in the class")

    def test_015_testing_port_setter_addition(self):
        """
        Tests that the port setter works for additions
        """
        print("\nStart testing port setter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class._all_ports, self.test_ports01)
        test_additional_ports = {
            "TCP": {
                "223": {"ERROR": "This is a test"},
                "225": {"ERROR": "This is a test"},
            },
            "UDP": {
                "223": {"ERROR": "This is a test"},
                "225": {"ERROR": "This is a test"},
            },
        }
        test_class.all_ports = test_additional_ports
        final_test_ports = {
            "TCP": {
                "20": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
                "23": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "25": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "37": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "43": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "53": {
                    "Domain_Name": "test.local",
                    "Server": "192.168.89.80",
                    "@": "[@ 604800 IN SOA @ root 2 604800 86400 2419200 604800][@ 604800 IN NS ns][@ 604800 IN A 192.168.89.80][@ 604800 IN AAAA ::1]",
                    "ns": "[ns 604800 IN A 192.168.89.80]",
                    "www": "[www 604800 IN A 192.168.89.80]",
                },
                "79": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
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
                "88": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "109": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "110": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "115": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "118": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "143": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "162": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "179": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "194": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "223": {"ERROR": "This is a test"},
                "225": {"ERROR": "This is a test"},
                "389": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "443": {
                    "Date": "Tue, 09 Mar 2021 13:09:42 GMT",
                    "Server": "Apache/2.4.41 (Ubuntu)",
                    "Last-Modified": "Tue, 23 Feb 2021 19:43:27 GMT",
                    "ETag": '"2ab0-5bc0621d8c961-gzip"',
                    "Accept-Ranges": "bytes",
                    "Vary": "Accept-Encoding",
                    "Content-Encoding": "gzip",
                    "Content-Length": "3145",
                    "Keep-Alive": "timeout=5, max=100",
                    "Connection": "Keep-Alive",
                    "Content-Type": "text/html",
                },
                "464": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "465": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "515": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "530": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "543": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "544": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "547": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "993": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "995": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "1080": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "3128": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "3306": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "3389": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "5432": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "5900": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "5938": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "8080": {
                    "Date": "Tue, 09 Mar 2021 13:09:45 GMT",
                    "Server": "Apache/2.4.41 (Ubuntu)",
                    "Last-Modified": "Tue, 23 Feb 2021 19:51:02 GMT",
                    "ETag": '"2abf-5bc063cf93aac-gzip"',
                    "Accept-Ranges": "bytes",
                    "Vary": "Accept-Encoding",
                    "Content-Encoding": "gzip",
                    "Content-Length": "3157",
                    "Keep-Alive": "timeout=5, max=100",
                    "Connection": "Keep-Alive",
                    "Content-Type": "text/html",
                },
                "8443": {
                    "Date": "Tue, 09 Mar 2021 13:09:44 GMT",
                    "Server": "Apache/2.4.41 (Ubuntu)",
                    "Last-Modified": "Mon, 08 Mar 2021 18:24:30 GMT",
                    "ETag": '"2abf-5bd0a8b7734dc-gzip"',
                    "Accept-Ranges": "bytes",
                    "Vary": "Accept-Encoding",
                    "Content-Encoding": "gzip",
                    "Content-Length": "3159",
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
                "67": {"ERROR": "Socket Timed Out"},
                "69": {"ERROR": "Socket Timed Out"},
                "88": {"ERROR": "Socket Timed Out"},
                "118": {"ERROR": "Socket Timed Out"},
                "123": {"ERROR": "Socket Timed Out"},
                "161": {"ERROR": "Socket Timed Out"},
                "162": {"ERROR": "Socket Timed Out"},
                "194": {"ERROR": "Socket Timed Out"},
                "223": {"ERROR": "This is a test"},
                "225": {"ERROR": "This is a test"},
                "464": {"ERROR": "Socket Timed Out"},
                "514": {"ERROR": "Socket Timed Out"},
                "530": {"ERROR": "Socket Timed Out"},
                "547": {"ERROR": "Socket Timed Out"},
                "995": {"ERROR": "Socket Timed Out"},
                "1080": {"ERROR": "Socket Timed Out"},
                "3389": {"ERROR": "Socket Timed Out"},
                "5938": {"ERROR": "Socket Timed Out"},
                "8080": {"ERROR": "Socket Timed Out"},
                "8443": {"ERROR": "Socket Timed Out"},
            },
        }
        self.assertEqual(len(test_class.all_ports), len(final_test_ports))
        for key in final_test_ports.keys():
            self.assertEqual(test_class.all_ports[key], final_test_ports[key])
            for port_key in final_test_ports[key].keys():
                self.assertEqual(
                    test_class.all_ports[key][port_key], final_test_ports[key][port_key]
                )
        for key in test_class.all_ports.keys():
            self.assertEqual(test_class.all_ports[key], final_test_ports[key])
            for port_key in test_class.all_ports[key].keys():
                self.assertEqual(
                    test_class.all_ports[key][port_key], final_test_ports[key][port_key]
                )
        print("Finish testing port setter works")

    def test_016_testing_port_getter(self):
        """
        Tests that the port getter works
        """
        print("\nStart testing port getter works")
        test_class = FoundDevice(self.test_ip01, self.test_time01)

        test_class.all_ports = self.test_ports01
        self.assertEqual(test_class.all_ports, self.test_ports01)
        print("Finish testing port getter works")

    def test_017_testing_port_setter_type_error(self):
        """
        Tests that the port setter raises correct errors
        """
        print("\nStart testing port setter raises correct errors")
        test_initial_ports = {
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
        }
        test_fail_ports_01 = {
            "TPC": {
                "515": {
                    "ERROR": "No connection could be made because the target machine actively refused it"
                },
            },
            "UPD": {
                "995": {"ERROR": "Socket Timed Out"},
            },
        }
        test_fail_ports_02 = {
            "TCP": [
                (1, 1),
                1,
                "a",
            ],
            "UDP": {
                (1, 1),
                1,
                "a",
            },
        }
        test_fail_03 = 1
        test_class_01 = FoundDevice(self.test_ip01, self.test_time01)
        test_class_02 = FoundDevice(self.test_ip01, self.test_time01)
        # catches Exception that Key is wrong name
        for key, value in test_fail_ports_01.items():
            with self.assertRaises(KeyError):
                test_class_01.all_ports = {key: value}
        # catches exception that is adding to .all_ports
        for key, value in test_fail_ports_02.items():
            with self.assertRaises(TypeError):
                test_class_01.all_ports = {key: value}
        # catches exception when creating .all_ports and dict value is not a dict
        for key, value in test_fail_ports_02.items():
            with self.assertRaises(TypeError):
                test_class_02.all_ports = {key: value}
        # catches TypeError for not a dictionary when adding to .all_ports
        for key, value in test_fail_ports_02.items():
            with self.assertRaises(TypeError):
                test_class_02.all_ports = {key: value}
        # catch error is passed a non-dict type from the beginning
        with self.assertRaises(TypeError):
            test_class_01.all_ports = test_fail_03
        print("Finish testing port setter raises raises correct errors")

    def test_018_response_time_not_tuple_of_floats(self):
        """
        Tests that a device creation fails because the tuple is not all floats
        """
        print("\nStart testing response time not a tuple is not all floats")
        test_time = (1.1, 1.35, 1)
        with self.assertRaises(TypeError):
            FoundDevice(self.test_ip01, test_time)
        test_time = (1.1, 1.35, "a")
        with self.assertRaises(TypeError):
            FoundDevice(self.test_ip01, test_time)
        test_time = (1.1, 1.35, [1, 1, 1])
        with self.assertRaises(TypeError):
            FoundDevice(self.test_ip01, test_time)
        test_time = (1.1, 1.35, {"a": 1, "b": 1, "c": 1})
        with self.assertRaises(TypeError):
            FoundDevice(self.test_ip01, test_time)
        print("Finish testing response time not a tuple is not all floats\n")

    def test_019_open_close_port_getters_pass(self):
        """
        Tests that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports passes for getter
        """
        print(
            "\nStart testing that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports passes for getter"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_ports = {
            "TCP": {
                "20": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
                "23": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
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
                "67": {"ERROR": "Socket Timed Out"},
            },
        }
        open_tcp_ports_dict = {
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
        }
        open_udp_ports_dict = {
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
            }
        }
        closed_tcp_ports_dict = {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
        }
        closed_udp_ports_dict = {
            "43": {"ERROR": "Socket Timed Out"},
            "67": {"ERROR": "Socket Timed Out"},
        }
        test_class.all_ports = test_ports
        self.assertEqual(test_class.closed_tcp_ports, closed_tcp_ports_dict)
        self.assertEqual(test_class.closed_udp_ports, closed_udp_ports_dict)
        self.assertEqual(test_class.open_tcp_ports, open_tcp_ports_dict)
        self.assertEqual(test_class.open_udp_ports, open_udp_ports_dict)
        print(
            "Finish testing that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports passes for getter\n"
        )

    def test_020_open_close_ports_fail_setting_directly(self):
        """
        Tests that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports will fail when trying to set directly
        """
        print(
            "\nStart testing that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports will fail when trying to set directly"
        )
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_ports = {
            "TCP": {
                "20": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
                "23": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
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
                "67": {"ERROR": "Socket Timed Out"},
            },
        }
        open_tcp_ports_dict = {
            "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
            "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
        }
        open_udp_ports_dict = {
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
            }
        }
        closed_tcp_ports_dict = {
            "20": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
            "23": {
                "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
            },
        }
        closed_udp_ports_dict = {
            "43": {"ERROR": "Socket Timed Out"},
            "67": {"ERROR": "Socket Timed Out"},
        }
        test_class.all_ports = test_ports
        with self.assertRaises(AttributeError):
            test_class.closed_tcp_ports = closed_tcp_ports_dict
        with self.assertRaises(AttributeError):
            test_class.closed_udp_ports = closed_udp_ports_dict
        with self.assertRaises(AttributeError):
            test_class.open_tcp_ports = open_tcp_ports_dict
        with self.assertRaises(AttributeError):
            test_class.open_udp_ports = open_udp_ports_dict
        print(
            "Finish testing that the property open_tcp_ports, open_udp_ports, closed_tcp_ports, and closed_udp_ports will fail when trying to set directly\n"
        )

    def test_021_class_str(self):
        """
        Tests that you class __str__ method is correct
        """
        print("\nStart testing that the __str__ method is correct")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        self.assertEqual(
            str(test_class),
            f"{self.test_ip01} : \n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms",
        )
        test_class.all_ports = self.test_ports01
        self.assertRegex(
            str(test_class),
            f"{self.test_ip01} : \n\tresponse times are {self.test_time01[0]} ms, {self.test_time01[1]} ms, {self.test_time01[2]} ms\n\tOpen TCP Ports:.*",
        )
        print("Finish testing that the __str__ method is correct\n")

    def test_022_json_short(self):
        """
        Tests that the json_short function works correctly
        """
        print("\nStart testing that the json_short function works correctly")
        test_class = FoundDevice(self.test_ip01, self.test_time01)
        test_string = {"192.168.1.65": {"ping_response_times": [1.1, 1.35, 1.82]}}
        self.assertEqual(test_class.print_json_short(), json.dumps(test_string))
        test_ports = {
            "TCP": {
                "20": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                },
                "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                "22": {"Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"},
                "23": {
                    "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
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
                "67": {"ERROR": "Socket Timed Out"},
            },
        }
        test_string = {
            "192.168.1.65": {
                "ping_response_times": [1.1, 1.35, 1.82],
                "Open_TCP_Ports_List": {
                    "21": {"Return Information": "220 (vsFTPd 3.0.3)"},
                    "22": {
                        "Return Information": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1"
                    },
                },
                "Open_UDP_Ports_List": {
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
                    }
                },
                "Closed_TCP_Ports_List": {
                    "20": {
                        "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                    },
                    "23": {
                        "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
                    },
                },
                "Closed_UDP_Ports_List": {
                    "43": {"ERROR": "Socket Timed Out"},
                    "67": {"ERROR": "Socket Timed Out"},
                },
            }
        }
        test_class.all_ports = test_ports
        self.maxDiff = None
        self.assertEqual(test_class.print_json_long(), json.dumps(test_string))

        print("Finish testing that the json_short function works correctly\n")


if __name__ == "__main__":
    unittest.main()
