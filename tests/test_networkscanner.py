#!python

"""
    THis will test the networkscanner and will contine to grow as time goes on
"""
import ipaddress
import unittest
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import networkscanner


class TestNetworkScanner(unittest.TestCase):
    """
    Tests that networkscanner works
    All other tests created have tested files.  This will test the individual functions them selves of the main file
    """

    def test_000_pass_get_who_to_scan_arglist_eq_1(self):
        print("\nStart testing that get_who_to_scan passes with arg_list of 1 argument")
        test_arg_list = [
            "c:/Users/copelaji/OneDrive - WWT/Python_Project/NetworkScanner/networkscanner.py"
        ]
        test_result = networkscanner.get_who_to_scan(test_arg_list)
        self.assertIsInstance(test_result, list)
        self.assertGreaterEqual(len(test_result), 1)
        for result in test_result:
            self.assertIsInstance(result, ipaddress.IPv4Address)
        print("Finish testing that get_who_to_scan passes with arg_list of 1 argument")

    def test_001_pass_get_who_to_scan_arglist_eq_0(self):
        print(
            "\nStart testing that get_who_to_scan passes with arg_list of 0 arguments"
        )
        test_arg_list = []
        with self.assertRaises(ValueError):
            networkscanner.get_who_to_scan(test_arg_list)
        print(
            "Finish testing that get_who_to_scan passes with arg_list of 0 arguments\n"
        )


if __name__ == "__main__":
    unittest.main()