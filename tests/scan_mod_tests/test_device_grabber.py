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

        print(
            "Finished the test that the check address function works as expected...\n"
        )


if __name__ == "__main__":
    unittest.main()
