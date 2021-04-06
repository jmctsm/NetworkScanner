#! python

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
import pytest


@pytest.mark.parametrize(
    "address, expected",
    [
        ("192.168.1.1", "192.168.1.1"),
        (ipaddress.ip_address("192.168.1.1"), "192.168.1.1"),
    ],
)
def test_01_all_pass(address, expected):
    assert check_address(address) == expected


@pytest.mark.parametrize(
    "address, exception_to_raise",
    [
        (None, ValueError),
        ("abc", ipaddress.AddressValueError),
        (1.1, TypeError),
    ],
)
def test_02_raise_exceptions(address, exception_to_raise):
    with pytest.raises(exception_to_raise):
        check_address(address)
