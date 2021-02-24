#!python

import ipaddress
import socket

# Protocol Scanner imports
from protocol_scanners.http_scanner import http_scanner
from protocol_scanners.https_scanner import https_scanner


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


def tcp_scanner(address, port):
    """
    Scans the TCP port and returns the string to the main function

    Args:
        address (str) : string of the IPv4 address that is passed from the calling function
        port (int) : int of the port to connect to

    Return:
        string of either the error message or the header from the port
    """
    if not isinstance(address, str):
        raise ValueError(f"{address} is not of type str")
    if not isinstance(port, int):
        raise ValueError(f"{port} is not of type int")
    print(f"Scanning TCP port {port}")
    if port == 80:
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
        output = (
            "No connection could be made because the target machine actively refused it"
        )
        print(f"TCP {port} = {output}")
        scan_socket.close()
        return output
    MESSAGE = b"Hello, World!"
    scan_socket.send(MESSAGE)
    try:
        scan_data = scan_socket.recv(1024).decode()
    except UnicodeDecodeError:
        scan_data = (
            "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
        )
        print(f"TCP {port} = {scan_data}")
        scan_socket.close()
        return scan_data
    else:
        print(f"TCP {port} = {scan_data.strip()}")
        scan_socket.close()
        return scan_data.strip()
    return None


def udp_scanner(address, port):
    """
    Scans the UDP port and returns the string to the main function

    Args:
        address (str) : string of the IPv4 address that is passed from the calling function
        port (int) : int of the port to connect to

    Return:
        string of either the error message or the header from the port
    """
    if not isinstance(address, str):
        raise ValueError(f"{address} is not of type str")
    if not isinstance(port, int):
        raise ValueError(f"{port} is not of type int")
    print(f"Scanning UDP port {port}")
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


def port_scanner(address):
    """
    This will scan an address for standard ports to see what is open. If it is open, it will then grab a header if applicable.
    It returns a dictionary of ports and headers to the calling function

    Args:
        address (IPv4 address object) : IPv4 address object to scan

    Return:
        dict : dictionary of ports and headers that are open on the box
        None : if no ports are open or responding
    """
    TCP_PORTS = (
        20,
        21,
        22,
        23,
        25,
        37,
        43,
        53,
        79,
        80,
        88,
        109,
        110,
        115,
        118,
        143,
        162,
        179,
        194,
        389,
        443,
        464,
        465,
        515,
        530,
        543,
        544,
        547,
        993,
        995,
        1080,
        3128,
        3306,
        3389,
        5432,
        5900,
        5938,
        8080,
    )
    UDP_PORTS = (
        43,
        53,
        67,
        69,
        88,
        118,
        123,
        161,
        162,
        194,
        464,
        514,
        530,
        547,
        995,
        1080,
        3389,
        5938,
        8080,
    )
    # check to make sure that the address is correct first
    if not isinstance(address, ipaddress.IPv4Address):
        raise ValueError(f"{address} since it is not an IPv4Address")
    return_dict = {}
    # Scan the TCP Ports
    print(f"SCANNING TCP PORTS for {address}...")
    for port in TCP_PORTS:
        TCP_key = f"TCP_{str(port)}"
        return_dict[TCP_key] = tcp_scanner(str(address), port)

    # Scan the UDP Ports
    print(f"SCANNING UDP PORTS for {address}...")
    for port in UDP_PORTS:
        UDP_key = f"UDP_{str(port)}"
        return_dict[UDP_key] = udp_scanner(str(address), port)

    return return_dict


if __name__ == "__main__":
    # calling function for example
    address_list = [
        ipaddress.ip_address("192.168.1.65"),
        ipaddress.ip_address("10.0.1.254"),
    ]
    dict_of_ports = {}
    for address in address_list:
        dict_of_ports[address] = port_scanner(address)
    print(dict_of_ports)