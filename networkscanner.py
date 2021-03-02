#!python

"""
    This is the main part of the NetworkScanner application.  This is where as things are added you will 
        see things added here.

    Basically, the user kicks off the program (which will be static at first) and then start doing the work
        1) It will ping using pinger
        2) all devices that are up are added as a device class
        3) all devices that are a device class are port scanned for specific ports
"""
"""
    TODO:
        Make a help function
        get_who_to_scan function
            Create arguments to get either a subnet or address from the command line
            Create arguments to add reading in a CSV file

"""

# Temporary Imports
import pprint

# Needed Imports
import sys
import ipaddress
import time


# Imports of Modules for this App
from scan_mods.pinger import pinger
from scan_mods.device_class import FoundDevice


def main():
    """
    This function will be the main function of the program.  It will call all other pieces of the application
    """
    argument_list = sys.argv
    who_to_scan = get_who_to_scan(argument_list)
    print("Starting the program.  Let the magic fly")

    # call the pinger program
    print("Pinging the hosts to see who is up")
    hosts_that_are_up = pinger(who_to_scan)

    # create a class instance of each device that is up
    print("We now know who is up.  Working on keeping that data")
    device_list = []
    for key, value in hosts_that_are_up.items():
        device = FoundDevice(key, value["ping"])
        device_list.append(device)


def get_who_to_scan(arg_list):
    """
    This function will somehow get the list of who to scan.  It will use the argument list of argv passed from main
    if the list is length of 1, then no args are there so use test addresses

    Args:
        arg_list (list) : list of the arguments passed from the command line

    Returns:
        (list) : list of the individual addresses to run against
    """
    if len(arg_list) == 0:
        raise ValueError(
            "There were no arguments passed to the function.  That is wrong.  Closing"
        )

    elif len(arg_list) == 1:
        print("No arguments were given so using a test set of addresses")
        test_addresses = [
            "192.168.1.64/29",
            "192.168.1.65",
            "192.168.89.0/24",
        ]
    else:
        print("I am not ready for anything other than just running the program yet")
    return_addresses = []
    for address in test_addresses:
        if "/" in address:
            address_obj = ipaddress.IPv4Network(address)
            for address_host in address_obj.hosts():
                return_addresses.append(address_host)
        else:
            address_obj = ipaddress.IPv4Address(address)
            return_addresses.append(address_obj)
    for address in return_addresses:
        if not isinstance(address, ipaddress.IPv4Address):
            raise TypeError(f"{address} is not an IPv4 address object.")
    if len(return_addresses) > 0:
        return return_addresses
    else:
        raise ValueError("No usable addresses to scan")


if __name__ == "__main__":
    startTime = time.time()
    main()
    executionTime = time.time() - startTime
    print(f"Execution time in minutes: {str(executionTime/60)}")
