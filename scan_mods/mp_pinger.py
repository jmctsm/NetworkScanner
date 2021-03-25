#!python

import ipaddress
from pythonping import ping
import re
import multiprocessing
import time


def __ping_address(address):
    """
    This will take an IP address in the IP objects and ping it.
    It will return either a string that says it timed out or it
    return a tuple of the address and response times

    This is pseudo private and should be called from the main pinger function.

    Tried to optomize so it can be run in a multi-processor environment

    Args:
        address (ipaddress.IPv4Address) : ipaddress in ipaddress.ipv4address class type

    Return:
        tuple/str : tuple of ip address and response times if the system is up or a TIMEOUT string if not
    """
    if not isinstance(address, ipaddress.IPv4Address):
        raise ValueError(f"{address} since it is not an IPv4Address")
    print(f"Pinging {address}", end=" (")
    result = ping(str(address), timeout=1, count=3)
    timeout_pattern = "Round Trip Times min/avg/max is 1000/1000.0/1000 ms"
    timeout_result = re.search(timeout_pattern, str(result), re.IGNORECASE)
    active_result = False
    if timeout_result:
        print("Not Responding)")
        return "TIMEOUT"
    else:
        active_pattern = "Round Trip Times min\/avg\/max is (.*)\/(.*)\/(.*) ms"
        active_result = re.search(active_pattern, str(result), re.IGNORECASE)
    if active_result:
        up_result = (
            float(active_result.group(1)),
            float(active_result.group(2)),
            float(active_result.group(3)),
        )
        print(f"{up_result[0]} ms, {up_result[1]} ms, {up_result[2]} ms)")
        return (address, up_result)


def pinger(addresses):
    """
    This will take a list of IP addresses in the IP objects and ping them.
    It will return a dictionary of addresses that are reachable along with
    the response times for each address.

    Args:
        addresses (list) : list of IP address objects to ping

    Return:
        list : list of IP address objects that are reachable and the
            response time of each one
    """
    # raise an error is an empty list is passed to the function
    if len(addresses) <= 0:
        raise ValueError(
            "Looks like the network didn't work for getting IPs.  Bye Bye!!"
        )
    if not isinstance(addresses, list):
        raise TypeError(
            "Looks like a list was not passed to pinger.  Please try again."
        )
    for address in addresses:
        if not isinstance(address, ipaddress.IPv4Address):
            raise ValueError(f"{address} since it is not an IPv4Address")
    with multiprocessing.Pool() as pool:
        ping_results = pool.map(__ping_address, addresses)

    active_dict = {}
    if len(ping_results) == 0:
        raise ValueError("Nothing was alive.  Pick a subnet that has something alive")

    for item in ping_results:
        if item is None:
            raise ValueError("The return value was not correct.")
        if isinstance(item, str) and item == "TIMEOUT":
            continue
        if isinstance(item[1], tuple) and len(item[1]) == 3:
            active_dict[item[0]] = {"ping": item[1]}
        else:
            print(item)
            raise ValueError("The return value was not correct.")

    if len(active_dict) > 0:
        return active_dict
    else:
        raise Exception("Nothing was alive.  Pick a subnet that has something alive")


if __name__ == "__main__":
    start_time = time.time()
    # test this out with a home network
    test_addresses = [
        ipaddress.ip_network("192.168.1.64/29"),
        ipaddress.ip_address("192.168.1.65"),
        ipaddress.ip_network("192.168.89.0/24"),
    ]
    # host list to pass to the pinger function
    hosts_lists = []
    # iterate through all of the hosts within the address list and append that to the list of
    # hosts to ping
    for address in test_addresses:
        if isinstance(address, ipaddress.IPv4Network):
            for x in address.hosts():
                hosts_lists.append(x)
        elif isinstance(address, ipaddress.IPv4Address):
            hosts_lists.append(address)
    # if the length of the hosts_lists is 0, that means there are no IPs to scan and
    # something went wrong
    # else start the pinger
    if len(hosts_lists) == 0:
        raise ValueError(
            "Looks like the network didn't work for getting IPs.  Bye Bye!!"
        )
    else:
        active_hosts = pinger(hosts_lists)
    if len(active_hosts) > 0:
        print(active_hosts)
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")