#!python

""" 
    Connect to a web server and grab the HTTP headers
"""

from typing import Type
import requests
import ipaddress
from requests import adapters


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
    while True:
        try:
            response = session.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            break
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            break
        except Exception as err:
            print(f"Other error occurred: {err}")
            break
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
    session.close()
    return "HTTP SERVER returned an error"


if __name__ == "__main__":
    for address in ["192.168.1.65", "192.168.89.80"]:
        print(http_scanner(address))
