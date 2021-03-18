#!python

"""
will be used to validate if an address is a valid IP address
"""

import ipaddress
import time


def check_address(address):
    """
    Checks to see if the address is a string or a ipaddress.IPv4Address type
    Checks to make sure that it is valid
    If all good, returns an address string
    If bad, raises exception
    Args:
        address (ipaddress.IPv4Address or string) : IPv4 address of ipaddress.IPv4Address type that will be used to connect to
    return:
        string : address string
    """
    if address is None:
        raise ValueError(f"No address was given.  Please don't do that again.")
    if isinstance(address, str):
        try:
            ipaddress.IPv4Address(address)
        except ipaddress.AddressValueError:
            raise ipaddress.AddressValueError(
                f"{address} is not set up to be an IPv4 adddress."
            )
        else:
            return address
    if isinstance(address, ipaddress.IPv4Address):
        return str(address)
    raise TypeError(f"{address} is not a viable address type")


if __name__ == "__main__":
    start_time = time.time()
    address_list_to_test = [
        ipaddress.ip_address("192.168.89.80"),
        ipaddress.ip_address("192.168.89.254"),
        "192.168.1.1",
        "192.168.1.65",
        1.1,
        1,
        "abc",
        None,
    ]
    for address in address_list_to_test:
        try:
            print(f"{check_address(address=address)} is a valid address")
        except ValueError as ex:
            print(ex)
        except ipaddress.AddressValueError as ex:
            print(ex)
        except TypeError as ex:
            print(ex)

    duration = time.time() - start_time
    print(f"Duration to run was {duration}")
