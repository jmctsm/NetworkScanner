#!python

""" 
    Connect to a web server and grab the HTTPS headers
"""

from typing import Type
import requests
import ipaddress
from requests import adapters
import time

# Disable the SSL warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def https_scanner(address):
    """
    This will connect to the HTTPS server and grab the headers for the HTTPS server

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
    session.mount("https://", adapter)
    url = f"https://{address}"
    while True:
        try:
            response = session.get(url, verify=False)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            session.close()
            return f"HTTPError -- {http_err}"
        except requests.exceptions.ConnectionError as conn_err:
            session.close()
            return f"ConnectionError -- {conn_err}"
        except Exception as err:
            session.close()
            return f"OtherError -- {err}"
        headers_dict = response.headers
        return_string = (
            f"Server : {headers_dict.get('Server', 'None Listed in Headers')}"
        )
        headers_dict.pop("Server", None)
        for key in headers_dict.keys():
            return_string += (
                f"\n\t{key} : {headers_dict.get(key, 'None Listed in Headers')}"
            )
        session.close()
        return return_string


if __name__ == "__main__":
    start_time = time.time()
    for address in ["192.168.1.65", "192.168.89.80"]:
        print(https_scanner(address))
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")