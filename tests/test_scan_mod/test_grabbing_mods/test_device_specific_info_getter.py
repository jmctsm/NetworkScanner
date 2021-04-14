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
                # add assertions here for results
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
                # add assertions here for results
        print("Finished test for all pass\n")