#!python

""" 
    Connect to a DNS server and get SOA record
"""
import dns.resolver
import ipaddress
import dns.query
import dns.zone
import time
import json


def strip_alligators(string):
    """
        This will strip all < > from a string and return it so that a JSON linter quits barking at me

    Args:
        string (str) : string to strip

    Return:
        string : original strin minus < and >
    """
    try:
        first_replace = str(string).replace("<", "[")
        second_replace = first_replace.replace(">", "]")
    except TypeError:
        return f"Cannot convert to a string to remove '<' or '>'"
    return second_replace


def validate_server_domain_name(server, domain_name):
    """
        Validates the server and domain_name variables

        Args:
            server (str) : string of an IP address to test the domain against
        domainname (str) : string for the domain to test against

    Return:
        tuple : tuple of the server and the domain name if they both validate correctly
    """
    if server is not None and not isinstance(server, str):
        raise ValueError(
            f"a server was passed of type {type(server)} but it needs to be of type str"
        )
    if server is not None:
        try:
            ipaddress.ip_address(server)
        except ValueError:
            raise ValueError(f"{server} does not appear to be an IPv4 or IPv6 address")
    if domain_name is not None and not isinstance(domain_name, str):
        raise ValueError(
            f"a domain was passed of type {type(server)} but it needs to be of type str"
        )
    if server is None:
        print(f"No server specified.  Using 192.168.89.80 for DNS resolution")
        return_server = "192.168.89.80"
    else:
        return_server = server
    if domain_name is None:
        print(f"No domain name specified.  Using test.local for DNS resolution")
        return_domain_name = "test.local"
    else:
        return_domain_name = domain_name

    return (return_server, return_domain_name)


def udp_dns_scanner(dns_server=None, domainname=None):
    """
    Will connect to and get information from the DNS device using udp

    Args:
        server (str) : optional string of an IP address to test the domain against\
        domainname (str) : optional string for the domain to test against

    Return:
        dict : dict of either a problem or a dict of the answers from the server

    """
    server_list = []
    return_dict = {}
    server, domain_name = validate_server_domain_name(dns_server, domainname)
    server_list.append(server)
    if len(server_list) > 1 or len(server_list) < 1:
        raise ValueError(
            f"Too Many servers.  Should have only been 1.  It was {len(server_list)}.  Aborting"
        )
    udp_resolver = dns.resolver.Resolver(configure=False)
    udp_resolver.nameservers = server_list
    try:
        response = udp_resolver.resolve(domain_name, "SOA")
    except dns.resolver.NoNameservers:
        return_dict = {
            "ERROR": f"DNSNoNameServers -- {server} failed to answer the query for {domain_name}"
        }
        return return_dict
    except dns.exception.Timeout:
        return_dict = {
            "ERROR": f"DNSTimeOutDNS -- operation timed out.  Port is more than likely blocked or not open"
        }
        return return_dict
    except dns.resolver.NoAnswer:
        return_dict = {
            "ERROR": f"DNSNoAnswer -- DNS response does not contain an answer to the query: {domain_name} IN SOA"
        }
        return return_dict
    except dns.resolver.NXDOMAIN:
        return_dict = {
            "ERROR": f"DNSNXDOMAIN -- The DNS query name does not exist: {domain_name}"
        }
        return return_dict
    for key, value in response.__dict__.items():
        if key == "rdtype":
            return_dict["Record Type"] = value.name
        elif key == "rdclass":
            return_dict["Record Class"] = value.name
        elif isinstance(response.__dict__.get(key, None), str):
            return_dict[key] = value
        elif isinstance(response.__dict__.get(key, None), int):
            return_dict[key] = str(response.__dict__.get(key, None))
        elif isinstance(response.__dict__.get(key, None), float):
            return_dict[key] = str(response.__dict__.get(key, None))
        elif isinstance(value, dns.message.ChainingResult):
            # return_dict["Answer"] = value.answer
            return_dict["Answer"] = strip_alligators(value.answer)
            return_dict["Canonical Name"] = strip_alligators(value.canonical_name)
            return_dict["Minimum TTL"] = strip_alligators(value.minimum_ttl)
            return_dict["CNAMES"] = value.cnames
        elif isinstance(value, dns.rrset.RRset):
            return_dict["DNS Record Set"] = value.__str__()
        elif isinstance(value, dns.name.Name):
            return_dict["Name"] = value.__str__()
    return return_dict


def tcp_dns_scanner(dns_server=None, domainname=None):
    """
    Will connect to and get information from the DNS device using tcp

    Args:
        server (str) : optional string of an IP address to test the domain against
        domainname (str) : optional string for the domain to test against

    Return:
        str : string of either a problem or a string of the answers from the server

    """
    server, domain_name = validate_server_domain_name(dns_server, domainname)
    return_dict = {}
    try:
        z = dns.zone.from_xfr(dns.query.xfr(server, domain_name))
    except dns.xfr.TransferError:
        return_dict = {
            "ERROR": f"DNSTransferError -- Zone Transfer Error for {domain_name} on server {server}"
        }
        return return_dict
    except ConnectionRefusedError:
        return_dict = {
            "ERROR": "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
        }
        return return_dict
    except ConnectionResetError:
        return_dict = {
            "ERROR": "ConnectionResetError -- An existing connection was forcibly closed by the remote host"
        }
        return return_dict
    except dns.exception.FormError:
        return_dict = {"ERROR": "DNSFormError -- No answer or RRset not for name"}
        return return_dict
    except TimeoutError as ex:
        return_dict = {"ERROR": f"TimeoutError -- {ex}"}
        return return_dict
    return_dict["Domain_Name"] = domain_name
    return_dict["Server"] = server
    for node in sorted(z.nodes.keys()):
        split_lines = z[node].to_text(node).splitlines()
        return_string = ""
        for entry in split_lines:
            return_string += f"[{entry}]"
        if isinstance(node, dns.name.Name):
            return_dict[node.__str__()] = return_string
        else:
            return_dict[node] = return_string
    return return_dict


if __name__ == "__main__":
    start_time = time.time()
    local_dns_server = [
        "192.168.1.65",
        "192.168.89.80",
    ]
    dict_of_ports = {}
    local_domain_name = ["test.local", "www.google.com", "google.com", "test.test"]
    for dns_server in local_dns_server:
        for domain in local_domain_name:
            dict_of_ports[f"{str(dns_server)}_UDP_{domain}"] = udp_dns_scanner(
                dns_server, domain
            )
            dict_of_ports[f"{str(dns_server)}_TCP_{domain}"] = tcp_dns_scanner(
                dns_server, domain
            )
    print(dict_of_ports)
    for key in dict_of_ports.keys():
        print(f"{key} = {dict_of_ports[key]}")
    print(f"\n\n\n{json.dumps(dict_of_ports)}")
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")
