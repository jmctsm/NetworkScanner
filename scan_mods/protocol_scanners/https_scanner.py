#!python

""" 
    Connect to a web server and grab the HTTPS headers
"""

import requests
import ipaddress
import time
import json

# Disable the SSL warning
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def https_scanner(address, port=None):
    """
    This will connect to the HTTPS server and grab the headers for the HTTPS server

    Args:
        address (str) : string of the address to connect to (IPv4 format)
        port (int) : will run the scanner against the port specified.  None given, it uses 443

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
    if port is not None:
        if not isinstance(port, int):
            if isinstance(port, float):
                raise TypeError(f"{port} is not an int and cannot be made into an int.")
            try:
                int(port)
            except ValueError:
                raise ValueError(
                    f"{port} is not an int and cannot be made into an int."
                )
            except TypeError:
                raise TypeError(f"{port} is not an int and cannot be made into an int.")
        elif int(port) < 0 or int(port) > 65535:
            raise ValueError(f"Port number has to be between 0 and 65535.")
    elif port is None:
        port = 443
    session = requests.Session()
    retry = requests.packages.urllib3.util.retry.Retry(connect=3, backoff_factor=0.5)
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    url = f"https://{address}:{port}"
    return_dict = {}
    while True:
        try:
            response = session.get(url, verify=False)
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
        dict_of_responses[address] = https_scanner(address)
    print(dict_of_responses)
    print("\n\n\n\n")
    print(json.dumps(dict_of_responses))
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")