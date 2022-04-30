import time
import socket
import struct
import random
from datetime import datetime

ICMP_ECHO_REQUEST = 8
TIMEOUT = 1
IP_HEADER_SIZE = 20

ICMP_CODE = socket.getprotobyname('icmp')

BASE = 16
BASIC_BYTES = 2
MAX_BYTES = 2 ** BASE - 1


def compute_checksum(data):
    checksum = 0
    for i in range(0, len(data), BASIC_BYTES):
        checksum += int.from_bytes(data[i:i + BASIC_BYTES], 'little')
    while checksum & MAX_BYTES != checksum:
        checksum = (checksum >> BASE) + (checksum & MAX_BYTES)
    return MAX_BYTES ^ checksum


def verify_checksum(data):
    return compute_checksum(data) == 0


def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 0)
    data = str(datetime.now()).encode('utf-8')
    my_checksum = compute_checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                         socket.htons(my_checksum), id, 1)
    return header + data


def do_one_ping(dest_addr, timeout=1):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        my_socket.settimeout(TIMEOUT)
    except Exception:
        print('Cannot start server!')
        return
    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id)
    while packet:
        sent = my_socket.sendto(packet, (dest_addr, 1))
        packet = packet[sent:]
    delay = receive_ping(my_socket, packet_id, time.time())
    my_socket.close()
    return delay


def receive_ping(my_socket, packet_id, time_sent):
    while True:
        try:
            rec_packet, addr = my_socket.recvfrom(1024)
            payload = rec_packet[IP_HEADER_SIZE:]
            if not verify_checksum(payload):
                print('Checksum verification failed')
                return
            time_received = time.time()
            icmp_header = rec_packet[20:28]
            type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
            if p_id == packet_id:
                return time_received - time_sent
        except socket.timeout:
            print('Request timed out')
            return


def verbose_ping(dest_addr, timeout=TIMEOUT, count=4):
    for i in range(count):
        'Ping {}...'.format(dest_addr),
        delay = do_one_ping(dest_addr, timeout)
        if delay is None:
            print(f'failed. (Timeout within {timeout} seconds.)')

        else:
            delay = round(delay * 1000.0, 4)
            print(f'Get ping in {delay} milliseconds')
        time.sleep(1)


if __name__ == '__main__':
    print('Pinging huawei.com ...')
    verbose_ping('huawei.com')
    print('====')
    print('Pinging 162.216.229.17 ...') #сервер компании World of Tanks в Вашингтоне
    verbose_ping('162.216.229.17')
