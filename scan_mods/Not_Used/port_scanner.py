#!python

import ipaddress
import socket
import time
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# Protocol Scanner imports
from scan_mods.protocol_scanners.http_scanner import http_scanner
from scan_mods.protocol_scanners.https_scanner import https_scanner
from scan_mods.protocol_scanners.dns_scanner import udp_dns_scanner
from scan_mods.protocol_scanners.dns_scanner import tcp_dns_scanner


"""

    TODO:  Might want to make different scanners for each of the different types of ports to make it easier to really get a good read on what they are


    This will take a list of IPV4 addresses and do a basic port scan on them.  The ports to see if they are open are below.  If they are open, the header will
    be grabbed and returned to the calling function.

    Ports to scan
        20: File Transfer Protocol (FTP) data channel.
        21: File Transfer Protocol (FTP) control channel. The commands port.
        22: Secure Shell (SSH). Remote management protocol OS.
        23: Telnet, or terminal network, for protocol implementation text interface across a network.
        25: Simple Mail Transfer Protocol (SMTP).
        37: Time protocol.
        43: WHOIS. Protocol for obtaining registration of ownership details for IP addresses and domain names.
        53: Domain Name System (DNS).
        67: Dynamic Host Configuration Protocol (DHCP). Dynamic IP.
        69: Trivial File Transfer Protocol (TFTP).
        79: Finger protocol.
        80: Hypertext Transfer Protocol (HTTP).
        88: Kerberos.
        109: Post Office Protocol v2 (POP2). Protocol for receiving emails, version two.
        110: Post Office Protocol v3 (POP3). Protocol for receiving emails, version three.
        115: Secure File Transfer Protocol (SFTP). Protocol for secure transmission of data.
        118: SQL Services.
        123: Network Time Protocol (NTP)
        143: Internet Message Access Protocol (IMAP). Protocol at the application level, for accessing emails.
        161: Simple Network Management Protocol (SNMP). Protocol for device management.
        162: Simple Network Management Protocol (SNMP) Trap.
        179: Border Gateway Protocol (BGP).
        194: Internet Relay Chat (IRC).
        389: Lightweight Directory Access Protocol (LDAP). Application layer protocol.
        443: Hypertext Transfer Protocol Secure (HTTPS). HTTP protocol, with support for encryption.
        464: Kerberos reset password.
        465: Simple Mail Transfer Protocol over SSL (SMTPS).
        514: Syslog.
        515: Line Printer Daemon (LPD). Protocol for remote printing.
        530: Remote Procedure Call (RPC).
        543: Kerberos login.
        544: Real Time Stream Control Protocol (RTSP).
        547: DHCPv6 server.
        993: Internet Message Access Protocol over SSL (IMAPS). IMAP protocol with support for SSL encryption.
        995: Post Office Protocol 3 over SSL (POP3S). POP3 protocol with support for SSL encryption.
        1080: SOCKet Secure (SOCKS). Protocol for receiving secure and anonymous access.
        3128: Proxy. Port often used for proxies.
        3306: MySQL, for MySQL database.
        3389: Remote Desktop Protocol (RDP), for Windows.
        5432: Postgres Database (PostgreSQL).
        5900: Virtual Network Computing (VNC). For desktop remote access.
        5938: TeamViewer, for the remote-control system, to facilitate data computer and data exchange.
        8080: HTTP/Web. An alternate HTTP protocol port.
"""


def __validate_for_scanners(address, port, domain):
    """
    Validates that the address, port, and domain are of the correct types
    Pulled here since the code was the same

    Args:
        address (str) : string type address
        port (int) : port number that should be an int
        domain (str) : domain name that should be a string
    """
    if not isinstance(address, str):
        raise TypeError(f"{address} is not of type str")
    if not isinstance(port, int):
        raise TypeError(f"{port} is not of type int")
    if domain is not None and not isinstance(domain, str):
        raise TypeError(f"{domain} is not a string")
    return True


def tcp_scanner(address, port, domain_name=None):
    """
    Scans the TCP port and returns the string to the main function

    Args:
        address (str) : string of the IPv4 address that is passed from the calling function
        port (int) : int of the port to connect to
        domain_name (str): optional variable to hold for domain_name testing in things like DNS

    Return:
        string of either the error message or the header from the port
    """
    __validate_for_scanners(address, port, domain_name)
    print(f"Scanning TCP port {port}")
    if port == 53:
        if domain_name is None:
            scan_data = tcp_dns_scanner(dns_server=address)
        else:
            scan_data = tcp_dns_scanner(dns_server=address, domainname=domain_name)
        print(f"TCP {port} = {scan_data}")
        return scan_data
    elif port == 80:
        scan_data = http_scanner(address)
        print(f"TCP {port} = {scan_data.strip()}")
        return scan_data
    elif port == 443:
        scan_data = https_scanner(address)
        print(f"TCP {port} = {scan_data.strip()}")
        return scan_data
    elif port == 8080:
        scan_data = http_scanner(address)
        print(f"TCP {port} = {scan_data.strip()}")
        return scan_data
    scan_socket = socket.socket()
    try:
        scan_socket.connect((address, port))
    except ConnectionRefusedError:
        output = "ConnectionRefusedError -- No connection could be made because the target machine actively refused it"
        print(f"TCP {port} = {output}")
        scan_socket.close()
        return output
    except TimeoutError:
        output = f"TimeoutError -- A connection attempt failed because the connected party did not properly respond after a period of time"
        output += ", or established connection failed because connected host has failed to respond"
        print(f"TCP {port} = {output}")
        scan_socket.close()
        return output
    MESSAGE = b"Hello, World!"
    scan_socket.send(MESSAGE)
    try:
        scan_data = scan_socket.recv(1024).decode()
    except UnicodeDecodeError:
        scan_data = "UnicodeDecodeError -- 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
        print(f"TCP {port} = {scan_data}")
        scan_socket.close()
        return scan_data
    else:
        print(f"TCP {port} = {scan_data.strip()}")
        scan_socket.close()
        return scan_data.strip()
    return None


def udp_scanner(address, port, domain_name=None):
    """
    Scans the UDP port and returns the string to the main function

    Args:
        address (str) : string of the IPv4 address that is passed from the calling function
        port (int) : int of the port to connect to
        domain_name (str): optional variable to hold for domain_name testing in things like DNS

    Return:
        string of either the error message or the header from the port
    """
    __validate_for_scanners(address, port, domain_name)
    print(f"Scanning UDP port {port}")
    if port == 53:
        if domain_name is None:
            scan_data = udp_dns_scanner(dns_server=address)
        else:
            scan_data = udp_dns_scanner(dns_server=address, domainname=domain_name)
        print(f"UDP {port} = {scan_data}")
        return scan_data
    try:
        MESSAGE = b"Hello, World!"
        # socket.AF_INET is for the internet protocol and socket.sock_dgram is for UDP
        scan_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        scan_socket.sendto(MESSAGE, (address, port))
        scan_socket.settimeout(2)
        scan_data, addr = scan_socket.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"UDP {port} = {scan_data.strip()}")
        scan_socket.close()
        return scan_data.strip()
    except socket.timeout:
        scan_data = f"Socket Timed Out"
        print(f"UDP {port} = {scan_data}")
        scan_socket.close()
        return scan_data
    return None


def port_scanner(address, domain_name=None):
    """
    This will scan an address for standard ports to see what is open. If it is open, it will then grab a header if applicable.
    It returns a dictionary of ports and headers to the calling function

    Args:
        address (IPv4 address object) : IPv4 address object to scan
        domain_name (str) : string of the domain name to test with other places like DNS

    Return:
        dict : dictionary of ports and headers that are open on the box
        None : if no ports are open or responding
    """
    TCP_PORTS = (53,)
    UDP_PORTS = (53,)
    # check to make sure that the address is correct first
    if not isinstance(address, ipaddress.IPv4Address):
        raise TypeError(f"{address} since it is not an IPv4Address")
    if domain_name is not None and not isinstance(domain_name, str):
        raise TypeError(f"{domain_name} is not a string")
    return_dict = {
        "TCP": {},
        "UDP": {},
    }
    # Scan the TCP Ports
    print(f"SCANNING TCP PORTS for {address}...")
    for port in TCP_PORTS:
        TCP_key = str(port)
        if domain_name is None:
            scan_result = tcp_scanner(str(address), port)
        else:
            scan_result = tcp_scanner(str(address), port, domain_name)
        if len(scan_result) < 1:
            scan_result = "Nothing returned from the server"
        return_dict["TCP"][TCP_key] = scan_result

    # Scan the UDP Ports
    print(f"SCANNING UDP PORTS for {address}...")
    for port in UDP_PORTS:
        UDP_key = str(port)
        if domain_name is None:
            scan_result = udp_scanner(str(address), port)
        else:
            scan_result = udp_scanner(str(address), port, domain_name)
        if len(scan_result) < 1:
            scan_result = "***Nothing returned from the server***"
        return_dict["UDP"][TCP_key] = scan_result

    return return_dict


if __name__ == "__main__":
    start_time = time.time()
    # calling function for example
    address_list = [
        ipaddress.ip_address("192.168.1.65"),
        ipaddress.ip_address("10.0.1.254"),
        ipaddress.ip_address("192.168.89.80"),
    ]
    test_domain_names = [
        "test.local",
        "www.google.com",
        "google.com",
        "test.test",
        None,
    ]
    dict_of_ports = {}
    for address in address_list:
        for test_domain_name in test_domain_names:
            dict_of_ports[address] = port_scanner(address, test_domain_name)
    print(dict_of_ports)
    duration = time.time() - start_time
    print(f"Total time was {duration} seconds")