#!python

""" 
    Connect to a web server and grab the HTTP headers
"""

from typing import Type
import requests
import ipaddress
import time
import json


def http_scanner(address):
    """
    This will connect to the HTTP server and grab the headers for the HTTP server

    Args:
        address (str) : string of the address to connect to (IPv4 format)

    Return:
        str : headers string formatted

    """
    if not isinstance(address, str):
        raise TypeError(f"{address} is not a string")
    try:
        ipaddress.IPv4Address(address)
    except ipaddress.AddressValueError:
        raise ipaddress.AddressValueError(
            f"{address} is not set up to be an IPv4 adddress.  It did not have four octets."
        )
    session = requests.Session()
    retry = requests.packages.urllib3.util.retry.Retry(connect=3, backoff_factor=0.5)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    url = f"http://{address}"
    return_dict = {}
    while True:
        try:
            response = session.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            session.close()
            return_dict["ERROR"] = f"HTTPError -- {http_err}"
            return return_dict
        except requests.exceptions.ConnectionError as conn_err:
            session.close()
            return_dict["ERROR"] = f"ConnectionError -- {conn_err}"
            return return_dict
        except Exception as err:
            session.close()
            return_dict["ERROR"] = f"OtherError -- {err}"
            return return_dict
        for key in response.headers.keys():
            return_dict[key] = response.headers.get(key, "None Listed in Headers")
        session.close()
        return return_dict


if __name__ == "__main__":
    start_time = time.time()
    dict_of_responses = {}
    for address in ["192.168.1.65", "192.168.89.80", "10.0.1.1", "192.168.1.254"]:
        dict_of_responses[address] = http_scanner(address)
    print(dict_of_responses)
    print("\n\n\n\n")
    print(json.dumps(dict_of_responses))
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")
