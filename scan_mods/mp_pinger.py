#!python

import ipaddress
from pythonping import ping
import re
import multiprocessing
import time


def ping_address(address):
    """
    This will take an IP address in the IP objects and ping it.
    It will return either a string that says it timed out or it
    return a tuple of the address and response times

    This is pseudo private and should be called from the main pinger function.

    Tried to optomize so it can be run in a multi-processor environment

    Args:
        address (str) : ipaddress in string format

    Return:
        tuple/str : tuple of ip address and response times if the system is up or a TIMEOUT string if not
    """
    try:
        ipaddress.ip_address(address)
    except ValueError:
        raise ValueError(f"{address} is not an IPv4 address")
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
        addresses (list) : list of IP address strings to ping

    Return:
        dict : dictionary of IP address strings that are reachable and the
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
        try:
            ipaddress.ip_address(address)
        except ValueError:
            raise ValueError(f"{address} is not an IPv4 address")
    with multiprocessing.Pool() as pool:
        ping_results = pool.map(ping_address, addresses)

    active_dict = {}
    if len(ping_results) == 0:
        raise ValueError("Nothing was alive.  Pick a subnet that has something alive")

    for item in ping_results:
        if item is None:
            raise ValueError("The return value was not correct.")
        if isinstance(item, str) and item == "TIMEOUT":
            continue
        if isinstance(item[1], tuple) and len(item[1]) == 3:
            active_dict[item[0]] = {"ping_response_time": item[1]}
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
        "192.168.89.1",
        "192.168.89.2",
        "192.168.89.3",
        "192.168.89.4",
        "192.168.89.5",
        "192.168.89.6",
        "192.168.89.7",
        "192.168.89.8",
        "192.168.89.9",
        "192.168.89.10",
        "192.168.89.11",
        "192.168.89.12",
        "192.168.89.13",
        "192.168.89.14",
        "192.168.89.15",
        "192.168.89.16",
        "192.168.89.17",
        "192.168.89.18",
        "192.168.89.19",
        "192.168.89.20",
        "192.168.89.21",
        "192.168.89.22",
        "192.168.89.23",
        "192.168.89.24",
        "192.168.89.25",
        "192.168.89.26",
        "192.168.89.27",
        "192.168.89.28",
        "192.168.89.29",
        "192.168.89.30",
        "192.168.89.31",
        "192.168.89.32",
        "192.168.89.33",
        "192.168.89.34",
        "192.168.89.35",
        "192.168.89.36",
        "192.168.89.37",
        "192.168.89.38",
        "192.168.89.39",
        "192.168.89.40",
        "192.168.89.41",
        "192.168.89.42",
        "192.168.89.43",
        "192.168.89.44",
        "192.168.89.45",
        "192.168.89.46",
        "192.168.89.47",
        "192.168.89.48",
        "192.168.89.49",
        "192.168.89.50",
        "192.168.89.51",
        "192.168.89.52",
        "192.168.89.53",
        "192.168.89.54",
        "192.168.89.55",
        "192.168.89.56",
        "192.168.89.57",
        "192.168.89.58",
        "192.168.89.59",
        "192.168.89.60",
        "192.168.89.61",
        "192.168.89.62",
        "192.168.89.63",
        "192.168.89.64",
        "192.168.89.65",
        "192.168.89.66",
        "192.168.89.67",
        "192.168.89.68",
        "192.168.89.69",
        "192.168.89.70",
        "192.168.89.71",
        "192.168.89.72",
        "192.168.89.73",
        "192.168.89.74",
        "192.168.89.75",
        "192.168.89.76",
        "192.168.89.77",
        "192.168.89.78",
        "192.168.89.79",
        "192.168.89.80",
        "192.168.89.81",
        "192.168.89.82",
        "192.168.89.83",
        "192.168.89.84",
        "192.168.89.85",
        "192.168.89.86",
        "192.168.89.87",
        "192.168.89.88",
        "192.168.89.89",
        "192.168.89.90",
        "192.168.89.91",
        "192.168.89.92",
        "192.168.89.93",
        "192.168.89.94",
        "192.168.89.95",
        "192.168.89.96",
        "192.168.89.97",
        "192.168.89.98",
        "192.168.89.99",
        "192.168.89.100",
        "192.168.89.101",
        "192.168.89.102",
        "192.168.89.103",
        "192.168.89.104",
        "192.168.89.105",
        "192.168.89.106",
        "192.168.89.107",
        "192.168.89.108",
        "192.168.89.109",
        "192.168.89.110",
        "192.168.89.111",
        "192.168.89.112",
        "192.168.89.113",
        "192.168.89.114",
        "192.168.89.115",
        "192.168.89.116",
        "192.168.89.117",
        "192.168.89.118",
        "192.168.89.119",
        "192.168.89.120",
        "192.168.89.121",
        "192.168.89.122",
        "192.168.89.123",
        "192.168.89.124",
        "192.168.89.125",
        "192.168.89.126",
        "192.168.89.127",
        "192.168.89.128",
        "192.168.89.129",
        "192.168.89.130",
        "192.168.89.131",
        "192.168.89.132",
        "192.168.89.133",
        "192.168.89.134",
        "192.168.89.135",
        "192.168.89.136",
        "192.168.89.137",
        "192.168.89.138",
        "192.168.89.139",
        "192.168.89.140",
        "192.168.89.141",
        "192.168.89.142",
        "192.168.89.143",
        "192.168.89.144",
        "192.168.89.145",
        "192.168.89.146",
        "192.168.89.147",
        "192.168.89.148",
        "192.168.89.149",
        "192.168.89.150",
        "192.168.89.151",
        "192.168.89.152",
        "192.168.89.153",
        "192.168.89.154",
        "192.168.89.155",
        "192.168.89.156",
        "192.168.89.157",
        "192.168.89.158",
        "192.168.89.159",
        "192.168.89.160",
        "192.168.89.161",
        "192.168.89.162",
        "192.168.89.163",
        "192.168.89.164",
        "192.168.89.165",
        "192.168.89.166",
        "192.168.89.167",
        "192.168.89.168",
        "192.168.89.169",
        "192.168.89.170",
        "192.168.89.171",
        "192.168.89.172",
        "192.168.89.173",
        "192.168.89.174",
        "192.168.89.175",
        "192.168.89.176",
        "192.168.89.177",
        "192.168.89.178",
        "192.168.89.179",
        "192.168.89.180",
        "192.168.89.181",
        "192.168.89.182",
        "192.168.89.183",
        "192.168.89.184",
        "192.168.89.185",
        "192.168.89.186",
        "192.168.89.187",
        "192.168.89.188",
        "192.168.89.189",
        "192.168.89.190",
        "192.168.89.191",
        "192.168.89.192",
        "192.168.89.193",
        "192.168.89.194",
        "192.168.89.195",
        "192.168.89.196",
        "192.168.89.197",
        "192.168.89.198",
        "192.168.89.199",
        "192.168.89.200",
        "192.168.89.201",
        "192.168.89.202",
        "192.168.89.203",
        "192.168.89.204",
        "192.168.89.205",
        "192.168.89.206",
        "192.168.89.207",
        "192.168.89.208",
        "192.168.89.209",
        "192.168.89.210",
        "192.168.89.211",
        "192.168.89.212",
        "192.168.89.213",
        "192.168.89.214",
        "192.168.89.215",
        "192.168.89.216",
        "192.168.89.217",
        "192.168.89.218",
        "192.168.89.219",
        "192.168.89.220",
        "192.168.89.221",
        "192.168.89.222",
        "192.168.89.223",
        "192.168.89.224",
        "192.168.89.225",
        "192.168.89.226",
        "192.168.89.227",
        "192.168.89.228",
        "192.168.89.229",
        "192.168.89.230",
        "192.168.89.231",
        "192.168.89.232",
        "192.168.89.233",
        "192.168.89.234",
        "192.168.89.235",
        "192.168.89.236",
        "192.168.89.237",
        "192.168.89.238",
        "192.168.89.239",
        "192.168.89.240",
        "192.168.89.241",
        "192.168.89.242",
        "192.168.89.243",
        "192.168.89.244",
        "192.168.89.245",
        "192.168.89.246",
        "192.168.89.247",
        "192.168.89.248",
        "192.168.89.249",
        "192.168.89.250",
        "192.168.89.251",
        "192.168.89.252",
        "192.168.89.253",
        "192.168.89.254",
    ]
    # host list to pass to the pinger function
    # iterate through all of the hosts within the address list and append that to the list of
    # hosts to ping
    active_hosts = pinger(test_addresses)
    if len(active_hosts) > 0:
        print(active_hosts)
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")