#! python

import unittest
from unittest.mock import patch
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


from scan_mods.common_validation_checks.check_enable_password import (
    check_enable_password,
)


class TestCheckEnablePassword(unittest.TestCase):
    def test_01_all_pass(self):
        test_list = [
            ("cisco", "192.168.1.1", "cisco"),
            ("test", "192.168.0.1", "test"),
        ]
        for test_tuple in test_list:
            password, address, expected = test_tuple
            self.assertEqual(check_enable_password(password, address), expected)

    def test_02_raise_exceptions(self):
        test_list = [
            ("cisco", 1.1, ValueError),
        ]
        for test_tuple in test_list:
            password, address, exception_to_raise = test_tuple
            with self.assertRaises(exception_to_raise):
                check_enable_password(password, address)

    @patch("getpass.getpass")
    def test_03_test_input_logic_pass(self, getpw):
        getpw.return_value = "ciscocisco"
        self.assertEqual(check_enable_password(None, "192.168.1.1"), "ciscocisco")

    @patch("getpass.getpass")
    def test_04_test_input_logic_return(self, getpw):
        test_list = [
            (None, "test01", "test01"),
            (1, "test02", "test02"),
            (1.1, "test03", "test03"),
            ("", "test04", "test04"),
            (
                "asdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdfasdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdfasdlfjalsjdf;lajsdfljlaksjfklla;dlfasl;dfj;alsjdf;lajsdfl;jaslfdjl;asj;dflasjdlfj;alsdlf;asldfj;asldfj;lasjdfl;ajsfld;jasfdoasydfiahsidfasbfmasfjbasfbasbfbasfdbasbfkabsdkfjbaksjdbfkasbfkbaskfdjbaksfbkasbfkjasbdfkbasdkfbaksjfkasfjabfkjabsdfkbaskdkjasbdkfasdfasdf",
                "test05",
                "test05",
            ),
        ]
        for test_tuple in test_list:
            bad_return, true_return_value, test_value = test_tuple
            getpw.side_effect = [bad_return, true_return_value]
            self.assertEqual(check_enable_password(None, "192.168.1.1"), test_value)


if __name__ == "__main__":
    unittest.main()