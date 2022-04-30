import socket

ICMP_ECHO_REQUEST = 8
TIMEOUT = 1
IP_HEADER_SIZE = 20
ICMP_CODE = socket.getprotobyname('icmp')
BASE = 16
BASIC_BYTES = 2
MAX_BYTES = 2 ** BASE - 1
ICMP_ERRORS = {
    (3, 0): 'Network unreachable',
    (3, 1): 'Host unreachable',
    (3, 2): 'Port unavailable',
    (3, 4): 'Message fragmentation required',
    (3, 5): 'Source route is out of order',
    (3, 6): 'Destination network unknown',
    (3, 7): 'Destination host unknown',
    (3, 8): 'Host isolated',
    (3, 9): 'Communication with the destination network is administratively prohibited',
    (3, 10): 'Communication with the destination host is administratively prohibited',
    (3, 11): 'The network is not available for this type of service',
    (3, 12): 'The host is not available for this type of service',
    (3, 13): 'Communication is administratively prohibited by a filter',
    (3, 14): 'Hosts seniority violation',
    (3, 15): 'Seniority discrimination',
    (4, 0): 'The source was disabled: queue is full',
    (11, 0): 'Time limit exceeded when transferring',
    (11, 1): 'Time limit exceeded during assembly',
    (12, 0): 'Incorrect IP header',
    (12, 1): 'Required option missing'
}


def compute_checksum(data):
    checksum = 0
    for i in range(0, len(data), BASIC_BYTES):
        checksum += int.from_bytes(data[i:i + BASIC_BYTES], 'little')
    while checksum & MAX_BYTES != checksum:
        checksum = (checksum >> BASE) + (checksum & MAX_BYTES)
    return MAX_BYTES ^ checksum


def verify_checksum(data):
    return compute_checksum(data) == 0
