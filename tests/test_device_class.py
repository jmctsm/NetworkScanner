import unittest
import ipaddress
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from device_class import FoundDevice


class TestFoundDevice(unittest.TestCase):
    """
    Tests that the device class works for FoundDevice
    """

    def test_00_class_init_pass(self):
        """
        Tests that a device can be created passing only the init variables
        """
        print("\nStart testing that class init works")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertIsInstance(test_class, FoundDevice)
        self.assertEqual(test_class._IP, test_ip)
        self.assertEqual(test_class._response_time, test_time)
        self.assertIsNone(test_class._ports)
        print("Finish testing that class init works\n")

    def test_01_IP_getter_works(self):
        """
        Tests that the IP getter for the class is working
        """
        print("\nStart testing that class IP getter works")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertEqual(test_class.IP, test_ip)
        print("Finish testing that class IP getter works works\n")

    def test_02_response_time_getter_works(self):
        """
        Tests that the response time getter for the class is working
        """
        print("\nStart testing that class response time getter works")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertEqual(test_class.response_time, test_time)
        print("Finish testing that class response time getter works\n")

    def test_03_initialize_with_no_arguments(self):
        """
        Test to see what if can initialize the class with no arguments
        """
        print("\nStart testing that class init fails with no variables")
        with self.assertRaises(TypeError):
            test_class = FoundDevice()
        print("Finish testing that class init works\n")

    def test_04_response_time_not_tuple(self):
        """
        Tests that a device creation fails for response time not being a tuple
        """
        print("\nStart testing response time not a tuple")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = [1.1, 1.35, 1.82]
        with self.assertRaises(TypeError):
            FoundDevice(test_ip, test_time)
        print("Finish testing response time not a tuple\n")

    def test_05_IP_Address_wrong_object(self):
        """
        Tests that a device creation fails for the IP not being an IPv4 Address object
        """
        print("\nStart testing address not being an IPv4 Address object")
        test_ip = "192.168.1.65"
        test_time = (1.1, 1.35, 1.82)
        with self.assertRaises(TypeError):
            test_class = FoundDevice(test_ip, test_time)
        print("Finish testing address not being an IPv4 Address object\n")

    def test_06_set_response_time_directly(self):
        """
        Tests that you cannot set the response_time directly
        """
        print("\nStart testing that response_time cannot be set be directly")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        with self.assertRaises(AttributeError):
            test_class.response_time = 4
        print("Finish testing that response_time cannot be set be directly\n")

    def test_07_set_IP_directly(self):
        """
        Tests that you cannot set the IP directly
        """
        print("\nStart testing that IP cannot be set be directly")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        with self.assertRaises(AttributeError):
            test_class.IP = 4
        print("Finish testing that response_time cannot be set be directly\n")

    def test_08_class_hash_value(self):
        """
        Tests that you hash value returns the correct value
        """
        print("\nStart testing that the hash value returned is correct")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertEqual(hash(test_class), hash(test_ip))
        print("Finish testing that the hash value returned is correct\n")

    def test_09_class_bool_value(self):
        """
        Tests that you bool value returns the correct value
        """
        print("\nStart testing that the bool value returned is correct")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertTrue(bool(test_class))
        print("Finish testing that the bool value returned is correct\n")

    def test_10_class_eq_value_true(self):
        """
        Tests that you class __eq__ method returns True
        """
        print("\nStart testing that the __eq__ method returns True")
        test_ip01 = ipaddress.IPv4Address("192.168.1.65")
        test_time01 = (1.1, 1.35, 1.82)
        test_class01 = FoundDevice(test_ip01, test_time01)
        test_ip02 = ipaddress.IPv4Address("192.168.1.65")
        test_time02 = (1.82, 1.35, 1.1)
        test_class02 = FoundDevice(test_ip02, test_time02)
        test_ip03 = "192.168.1.65"
        self.assertTrue(test_class01 == test_class02)
        self.assertTrue(test_class01 == test_ip02)
        self.assertTrue(test_class01 == test_ip03)
        print("Finish testing that the __eq__ method returns True\n")

    def test_11_class_eq_value_false(self):
        """
        Tests that you class __eq__ method returns False
        """
        print("\nStart testing that the __eq__ method returns False")
        test_ip01 = ipaddress.IPv4Address("192.168.1.65")
        test_time01 = (1.1, 1.35, 1.82)
        test_class01 = FoundDevice(test_ip01, test_time01)
        test_ip02 = ipaddress.IPv4Address("192.168.1.66")
        test_time02 = (1.1, 1.35, 1.82)
        test_class02 = FoundDevice(test_ip02, test_time02)
        test_ip03 = "192.168.89.80"
        test_ip04 = "1.1.1"
        self.assertFalse(test_class01 == test_class02)
        self.assertFalse(test_class01 == test_ip02)
        self.assertFalse(test_class01 == test_ip03)
        self.assertFalse(test_class01 == test_ip04)
        print("Finish testing that the __eq__ method returns False\n")

    def test_12_class_repr(self):
        """
        Tests that you class __repr__ method is correct
        """
        print("\nStart testing that the __repr__ method is correct")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        self.assertEqual(
            repr(test_class),
            "192.168.1.65 : response times are 1.1 ms, 1.35 ms, 1.82 ms",
        )
        print("Finish testing that the __repr__ method is correct\n")

    def test_13_class_init_response_time_short(self):
        """
        Tests that a device creation fails if the tuple for response time is not length of 3
        """
        print(
            "\nStart testing that class init fails with response time is less than length of 3"
        )
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time_01 = (1.1, 1.35)
        with self.assertRaises(ValueError):
            FoundDevice(test_ip, test_time_01)
        test_time_02 = (1.1, 1.35, 1.56, 1.78, 1.96)
        with self.assertRaises(ValueError):
            FoundDevice(test_ip, test_time_02)
        print(
            "Finish testing that class init fails with response time is less than length of 3\n"
        )

    def test_14_testing_port_setter_empty(self):
        """
        Tests that the port setter works with an empty port list in the class
        """
        print("\nStart testing port setter works with an empty port list in the class")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        test_initial_ports = {
            "TCP_443": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Fri, 26 Feb 2021 10:59:10 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:43:27 GMT\n\tETag : "2ab0-5bc0621d8c961-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3145\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
        }
        test_class.ports = test_initial_ports
        self.assertEqual(test_class._ports, test_initial_ports)
        print("Finish testing port setter works with an empty port list in the class")

    def test_15_testing_port_setter_addition(self):
        """
        Tests that the port setter works
        """
        print("\nStart testing port setter works")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        test_initial_ports = {
            "TCP_443": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Fri, 26 Feb 2021 10:59:10 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:43:27 GMT\n\tETag : "2ab0-5bc0621d8c961-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3145\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
        }
        test_additional_ports = {
            "TCP_23": "No connection could be made because the target machine actively refused it",
            "TCP_25": "No connection could be made because the target machine actively refused it",
        }
        test_class.ports = test_initial_ports
        self.assertEqual(test_class._ports, test_initial_ports)
        test_class.ports = test_additional_ports
        final_test_ports = {
            "TCP_443": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Fri, 26 Feb 2021 10:59:10 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:43:27 GMT\n\tETag : "2ab0-5bc0621d8c961-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3145\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
            "TCP_23": "No connection could be made because the target machine actively refused it",
            "TCP_25": "No connection could be made because the target machine actively refused it",
        }
        self.assertEqual(len(test_class.ports), len(final_test_ports))
        for key in final_test_ports.keys():
            self.assertEqual(test_class.ports[key], final_test_ports[key])
        for key in test_class.ports.keys():
            self.assertEqual(final_test_ports[key], test_class.ports[key])
        print("Finish testing port setter works")

    def test_16_testing_port_getter(self):
        """
        Tests that the port getter works
        """
        print("\nStart testing port getter works")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        test_ports = {
            "TCP_443": 'Server : Apache/2.4.41 (Ubuntu)\n\tDate : Fri, 26 Feb 2021 10:59:10 GMT\n\tLast-Modified : Tue, 23 Feb 2021 19:43:27 GMT\n\tETag : "2ab0-5bc0621d8c961-gzip"\n\tAccept-Ranges : bytes\n\tVary : Accept-Encoding\n\tContent-Encoding : gzip\n\tContent-Length : 3145\n\tKeep-Alive : timeout=5, max=100\n\tConnection : Keep-Alive\n\tContent-Type : text/html',
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
        }
        test_class._ports = test_ports
        self.assertEqual(test_class.ports, test_ports)
        print("Finish testing port getter works")

    def test_17_testing_port_setter_value_error(self):
        """
        Tests that the port setter raises an value error
        """
        print("\nStart testing port setter raises an value error")
        test_fail_ports = {
            "TPC_515": "No connection could be made because the target machine actively refused it",
            "UPD_995": "Socket Timed Out",
            "TCP_515": 1,
            "UDP_995": 1.2,
        }
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1.82)
        test_class = FoundDevice(test_ip, test_time)
        for key, value in test_fail_ports.items():
            test_dict = {key: value}
            with self.assertRaises(ValueError):
                test_class.ports = test_dict
        test_initial_ports = {
            "TCP_515": "No connection could be made because the target machine actively refused it",
            "UDP_995": "Socket Timed Out",
            "UDP_1080": "Socket Timed Out",
        }
        test_class.ports = test_initial_ports
        for key, value in test_fail_ports.items():
            test_dict = {key: value}
            with self.assertRaises(ValueError):
                test_class.ports = test_dict
        print("Finish testing port setter raises an value error")

    def test_18_response_time_not_tuple_of_floats(self):
        """
        Tests that a device creation fails because the tuple is not all floats
        """
        print("\nStart testing response time not a tuple is not all floats")
        test_ip = ipaddress.IPv4Address("192.168.1.65")
        test_time = (1.1, 1.35, 1)
        with self.assertRaises(TypeError):
            FoundDevice(test_ip, test_time)
        test_time = (1.1, 1.35, "a")
        with self.assertRaises(TypeError):
            FoundDevice(test_ip, test_time)
        test_time = (1.1, 1.35, [1, 1, 1])
        with self.assertRaises(TypeError):
            FoundDevice(test_ip, test_time)
        test_time = (1.1, 1.35, {"a": 1, "b": 1, "c": 1})
        with self.assertRaises(TypeError):
            FoundDevice(test_ip, test_time)
        print("Finish testing response time not a tuple is not all floats\n")


if __name__ == "__main__":
    unittest.main()
