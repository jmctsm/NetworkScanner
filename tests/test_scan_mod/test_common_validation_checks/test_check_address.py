#! python

import unittest
import os
import sys

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


from scan_mods.common_validation_checks.check_address import check_address

import ipaddress


class TestCheckAddress(unittest.TestCase):
    def test_01_all_pass(self):
        test_dict = {
            ipaddress.ip_address("192.168.1.1"): "192.168.1.1",
            "192.168.1.1": "192.168.1.1",
        }
        for test_address, return_value in test_dict.items():
            self.assertEqual(check_address(test_address), return_value)

    def test_02_raise_exceptions(self):
        test_dict = {
            "test01": (None, ValueError),
            "test02": ("abc", ipaddress.AddressValueError),
            "test03": (1.1, TypeError),
        }
        for test_tuple in test_dict.values():
            test_address, exception_to_raise = test_tuple
            with self.assertRaises(exception_to_raise):
                check_address(test_address)


if __name__ == "__main__":
    unittest.main()