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
from multiprocessing import Value

# Needed Imports
import os
import sys
import ipaddress
import time
import argparse

# Imports of Modules for this App
from scan_mods.mp_pinger import pinger
from scan_mods.device_class import FoundDevice
import scan_mods.common_validation_checks.check_username
import scan_mods.common_validation_checks.check_password
import scan_mods.common_validation_checks.check_enable_password
import scan_mods.mp_port_scanner


def parse_my_args():
    """
    Parse the arguments and return a namespace of arguments
    return:
        dict : dictionary of namespace arguments
    """
    my_parser = argparse.ArgumentParser(
        description="Ping, scan, and grab configs from device(s)"
    )
    my_parser.add_argument(
        "-u",
        "--username",
        action="store",
        nargs="?",
        default="",
        help="Username to connect with to single box or subnet.  If not given, it will be asked for each box tested against",
        metavar="USERNAME",
    )
    my_parser.add_argument(
        "-p",
        "--password",
        action="store_true",
        help="Password to connect with to single box or subnet.  Will be asked for in a second",
    )
    my_parser.add_argument(
        "-e",
        "--enable",
        action="store_true",
        help="Enable password to connect with to single box or subnet.  Will be asked for in a second",
    )
    my_parser.add_argument(
        "-d",
        "--domain_name",
        action="store",
        nargs=1,
        help="Domain name to be used during testing",
        metavar="DOMAIN_NAME",
    )

    group = my_parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-c",
        "--csv",
        action="store",
        nargs=1,
        help="Input is a CSV file to grab information from for running against",
        metavar="CSV_FILE",
    )
    group.add_argument(
        "-a",
        "--address",
        action="store",
        nargs=1,
        help="single IP to run against",
        metavar="IP_ADDRESS",
    )
    group.add_argument(
        "-s",
        "--subnet",
        action="store",
        nargs=1,
        help="single subnet to run against",
        metavar="SUBNET",
    )

    return my_parser.parse_args()


def main():
    """
    This function will be the main function of the program.  It will call all other pieces of the application
    """
    print("Starting the program.  Let the magic fly")

    args = parse_my_args()

    list_of_addresses = ()

    if hasattr(args, "address") and args.address is not None:
        list_of_addresses = get_who_to_scan(args.address)
        address_dict, testing_addresses = create_scan_dictionary(
            args, list_of_addresses, args.address[0]
        )
    elif hasattr(args, "subnet") and args.subnet is not None:
        list_of_addresses = get_who_to_scan(args.subnet)
        address_dict, testing_addresses = create_scan_dictionary(
            args, list_of_addresses, args.subnet[0]
        )
    elif hasattr(args, "csv") and args.csv is not None:
        address_dict, testing_addresses = parse_csv_file(args.csv[0])
    # call the pinger program
    print("Pinging the hosts to see who is up")
    hosts_that_are_up = pinger(testing_addresses)
    # create a class instance of each device that is up
    print("We now know who is up.  Working on keeping that data")
    device_list = []
    for address, responsetime in hosts_that_are_up.items():
        device = FoundDevice(
            address,
            responsetime["ping_response_time"],
            address_dict[address]["username"],
            address_dict[address]["password"],
            address_dict[address]["use_enable"],
            address_dict[address]["enable_password"],
            address_dict[address]["domain_name"],
        )
        device_list.append(device)

    for device in device_list:
        device.get_ports()
        device.device_info_grabber()
        write_directory = None
        if "Output" in os.listdir(os.getcwd()):
            write_directory = f"{os.getcwd()}/Output/Scans/{device.IP}"
        else:
            path = "../"
            while write_directory is None:
                if "Output" in os.listdir(path):
                    write_directory = f"{path}/Output/Scans/{device.IP}"
                path += "../"
        if not os.path.exists(write_directory):
            os.makedirs(write_directory)
        file_location = f"{write_directory}\\{device.IP}_json_short.txt"
        with open(file_location, "w") as output_file:
            output_file.write(device.print_json_short())
        file_location = f"{write_directory}\\{device.IP}_json_long.txt"
        with open(file_location, "w") as output_file:
            output_file.write(device.print_json_long())


def get_who_to_scan(addresses_to_test):
    """
    This function will somehow get the list of who to scan.
    It will take the argument list passed from earlier to get valid addresses to scan.

    Args:
        addresses_to_test (list) : list of the addresses to test if valid IPv4 addresses

    Returns:
        (list) : list of the individual addresses to run against
    """
    if len(addresses_to_test) == 0:
        raise ValueError(
            "There were no arguments passed to the function.  That is wrong.  Closing"
        )

    return_addresses = []
    for address in addresses_to_test:
        if "/" in address:
            try:
                six_or_four = ipaddress.ip_network(address)
            except ValueError:
                print(f"{address} is not a valid subnet.  Skipping.")
                continue
            for address_host in six_or_four.hosts():
                return_addresses.append(str(address_host))
        else:
            try:
                ipaddress.ip_address(address)
            except ValueError:
                print(f"{address} is not a valid address.  Skipping.")
                continue
            return_addresses.append(str(address))
    for address in return_addresses:
        try:
            ipaddress.ip_address(address)
        except ValueError:
            raise ValueError(f"{address} is not an IPv4/v6 address. Shutting Down")
    if len(return_addresses) > 0:
        return return_addresses
    else:
        raise ValueError("No usable addresses to scan")


def create_scan_dictionary(script_args, address_list, address_space):
    """
    will create the scan dictionary of hosts, passwords, usernames, domain_names to pass later on to other functions
    Args:
        script_args (<class 'argparse.Namespace'>) : script command line arguments that will decide if need to get username and password and such
        address_list (list) : list of the IP addresses to scan
        address_space (str) : string of the address(es) user put in to scan
    return:
        list : list of addressesto test
        dict : dictionary of following format
            return_dict[address] = {"username":username,"password":password,"use_enable":use_enable,"enable_password":enable_password,"domain_name":domain_name,}
    """
    return_dict = {}
    for address in address_list:
        try:
            ipaddress.ip_address(address)
        except ValueError:
            raise ValueError(f"{address} is not a valid IP address")
    # if username is "" then that means the username flag was not used
    # if username is None, then username flag was set but nothing given.  Time to ask
    # if the username is not "" or None then user can a username

    if hasattr(script_args, "username"):
        if script_args.username == "":
            username = None
        else:
            username = scan_mods.common_validation_checks.check_username.check_username(
                script_args.username, address=address_space
            )
    else:
        username = None

    if hasattr(script_args, "password"):
        if script_args.password == False:
            password = None
        else:
            password = scan_mods.common_validation_checks.check_password.check_password(
                script_args.password, address=address_space
            )
    else:
        password = None

    if hasattr(script_args, "enable"):
        if script_args.enable is False:
            use_enable = False
            enable_password = None
        else:
            use_enable = True
            enable_password = scan_mods.common_validation_checks.check_enable_password.check_enable_password(
                script_args.enable, address=address_space
            )
    else:
        use_enable = False
        enable_password = None

    if hasattr(script_args, "domain_name"):
        if script_args.domain_name is None:
            domain_name = None
        else:
            domain_name = script_args.domain_name[0]
    else:
        domain_name = None

    for address in address_list:
        return_dict[address] = {
            "username": username,
            "password": password,
            "use_enable": use_enable,
            "enable_password": enable_password,
            "domain_name": domain_name,
        }
    return (return_dict, address_list)


def parse_csv_file(csv_file_location):
    """
    This will parse the CSV file passed at the command line
    Args:
        csv_file_location (string) : string of the path of the csv file
    return:
        list : list of addresses to test for pinger
        dict : dictionary of following format
            return_dict[address] = {"username":username,"password":password,"use_enable":use_enable,"enable_password":enable_password,"domain_name":domain_name,}

    """
    import csv

    return_dict = {}
    return_address_list = []
    with open(csv_file_location) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if row[0].startswith("#"):
                continue
            else:
                if len(row) != 6:
                    raise ValueError(
                        f"CSV file was not in the right format.  Start over."
                    )
                (
                    address,
                    username,
                    password,
                    domain_name,
                    enable_enabled,
                    enable_password,
                ) = row
                address_list = []
                address_list.append(address)
                address_list_parsed = get_who_to_scan(address_list)
                usable_username = (
                    scan_mods.common_validation_checks.check_username.check_username(
                        username, address=address
                    )
                )
                usable_password = (
                    scan_mods.common_validation_checks.check_password.check_password(
                        password, address=address
                    )
                )
                if domain_name == "":
                    usable_domain_name = None
                else:
                    usable_domain_name = domain_name
                if enable_enabled == "False":
                    use_enable = False
                    useable_enable_password = None
                else:
                    use_enable = True
                    useable_enable_password = scan_mods.common_validation_checks.check_enable_password.check_enable_password(
                        enable_password, address=address
                    )
                if len(address_list_parsed) == 0:
                    raise ValueError("No usable address in the CSV file.  Start over.")
                for add_item in address_list_parsed:
                    return_address_list.append(add_item)
                    return_dict[add_item] = {
                        "username": usable_username,
                        "password": usable_password,
                        "use_enable": use_enable,
                        "enable_password": useable_enable_password,
                        "domain_name": usable_domain_name,
                    }
    return (return_dict, return_address_list)


if __name__ == "__main__":

    import pprint

    startTime = time.time()
    main()
    executionTime = time.time() - startTime
    print(f"Execution time in minutes: {str(executionTime/60)}")
