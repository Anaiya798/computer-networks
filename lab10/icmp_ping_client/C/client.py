import time
import struct
import random
from datetime import datetime
from icmp import *
from statistics import calc_statistics


def create_packet(id):
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, 0)
    data = str(datetime.now()).encode('utf-8')
    my_checksum = compute_checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0,
                         socket.htons(my_checksum), id, 1)
    return header + data


def do_one_ping(dest_addr, port=1, timeout=1):
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP_CODE)
        my_socket.settimeout(TIMEOUT)
    except Exception:
        print('Cannot start server!')
        return
    packet_id = int((id(timeout) * random.random()) % 65535)
    packet = create_packet(packet_id)
    while packet:
        sent = my_socket.sendto(packet, (dest_addr, port))
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
                if type == 0:
                    return time_received - time_sent
                elif (type, code) in ICMP_ERRORS.items():
                    print(ICMP_ERRORS[(type, code)])
                    return
                else:
                    print('Unknown icmp error occured')
                    return

        except socket.timeout:
            print('Request timed out')
            return


def verbose_ping(dest_addr, timeout=TIMEOUT, count=4):
    try:
        socket.gethostbyname(dest_addr)
    except socket.gaierror:
        print(f'Unknown destination host: {dest_addr}')
        return 2

    rtts = []
    for i in range(1, count + 1):
        'Ping {}...'.format(dest_addr),
        delay = do_one_ping(dest_addr, timeout)
        if delay is None:
            print(f'failed. (Timeout within {timeout} seconds.)')

        else:
            delay = round(delay * 1000, 4)
            rtts.append(delay)
            print(f'Get ping in {delay} milliseconds')
            calc_statistics(i, rtts)
        time.sleep(1)


if __name__ == '__main__':
    print('Pinging huawei.com ...')
    verbose_ping('huawei.com')
    print('\n\n\n')
    print('Pinging 162.216.229.17 ...')  # сервер компании World of Tanks в Вашингтоне
    verbose_ping('162.216.229.17')
