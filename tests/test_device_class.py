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
            test_class = FoundDevice(test_ip, test_time)
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
        self.assertTrue(test_class01 == test_class02)
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
        self.assertFalse(test_class01 == test_class02)
        print("Finish testing that the __eq__ method returns False\n")

    def test_12_class_eq_value_true(self):
        """
        Tests that you class __eq__ method raises an Exception
        """
        print("\nStart testing that the __eq__ method raises an Exception")
        test_ip01 = ipaddress.IPv4Address("192.168.1.65")
        test_time01 = (1.1, 1.35, 1.82)
        test_class01 = FoundDevice(test_ip01, test_time01)
        test_ip02 = ipaddress.IPv4Address("192.168.1.65")
        with self.assertRaises(TypeError):
            test_class01 == test_ip02
        print("Finish testing that the __eq__ method raises an Exception\n")

    def test_13_class_repr(self):
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


if __name__ == "__main__":
    unittest.main()
