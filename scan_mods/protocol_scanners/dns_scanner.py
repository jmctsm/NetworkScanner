#!python

""" 
    Connect to a DNS server and get SOA record
"""
import dns.resolver
import ipaddress
import dns.query
import dns.zone


def udp_dns_scanner(dns_server=None, domainname=None):
    """
    Will connect to and get information from the DNS device using udp

    Args:
        server (str) : optional string of an IP address to test the domain against\
        domainname (str) : optional string for the domain to test against

    Return:
        str : string of either a problem or a string of the answers from the server

    """
    server_list = []
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
        return f"{server} failed to answer the query for {domain_name}"
    except dns.exception.Timeout:
        return f"DNS operation timed out.  Port is more than likely blocked or not open"
    except dns.resolver.NoAnswer:
        return f"DNS response does not contain an answer to the query: {domain_name} IN SOA"
    except dns.resolver.NXDOMAIN:
        return f"The DNS query name does not exist: {domain_name}"
    return_string = f"Canonical Name : {response.canonical_name}"
    response.__dict__.pop("canonical_name")
    for key, value in response.__dict__.items():
        if key == "rdtype":
            return_string += f"\n\tRecord Type = {value.name}"
        elif key == "rdclass":
            return_string += f"\n\tRecord Class = {value.name}"
        elif isinstance(response.__dict__.get(key, None), str):
            return_string += f"\n\t{key} = {value}"
        elif isinstance(response.__dict__.get(key, None), int):
            return_string += f"\n\t{key} = {str(response.__dict__.get(key, None))}"
        elif isinstance(response.__dict__.get(key, None), float):
            return_string += f"\n\t{key} = {str(response.__dict__.get(key, None))}"
        elif isinstance(value, dns.message.ChainingResult):
            return_string += f"\n\tAnswer = {value.answer}"
            return_string += f"\n\tMinimum TTL = {value.minimum_ttl}"
        elif isinstance(value, dns.rrset.RRset):
            return_string += f"\n\tDNS Record Set = {value}"
        elif isinstance(value, dns.name.Name):
            return_string += f"\n\tName = {value}"
    return return_string


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
    try:
        z = dns.zone.from_xfr(dns.query.xfr(server, domain_name))
    except dns.xfr.TransferError:
        return f"Zone Transfer Error for {domain_name} on server {server}"
    except ConnectionRefusedError:
        return "ConnectionRefusedError: No connection could be made because the target machine actively refused it"
    except ConnectionResetError:
        return "ConnectionResetError: An existing connection was forcibly closed by the remote host"
    except dns.exception.FormError:
        return "FormError: No answer or RRset not for name"
    except TimeoutError as ex:
        return f"TimeoutError: {ex}"
    return_string = f"Zone transfer for {domain_name} from server {server}"
    for node in sorted(z.nodes.keys()):
        split_lines = z[node].to_text(node).splitlines()
        for entry in split_lines:
            return_string += f"\n\t{entry}"
    return return_string


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


if __name__ == "__main__":
    local_dns_server = [
        "192.168.1.65",
        "192.168.89.80",
    ]
    local_domain_name = ["test.local", "www.google.com", "google.com", "test.test"]
    for dns_server in local_dns_server:
        for domain in local_domain_name:
            print(
                f"{dns_server}:{domain} <UDP> = {udp_dns_scanner(dns_server, domain)}"
            )
            print(
                f"{dns_server}:{domain} <TCP> = {tcp_dns_scanner(dns_server, domain)}"
            )
