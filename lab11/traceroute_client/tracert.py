from icmp import *

import socket
import struct
import time


def ping(dest_addr, icmp_socket, time_to_live, id, timeout, requests_count):
    addr = None
    print(f'{time_to_live:3}', end='\t')
    for _ in range(requests_count):
        try:
            initial_checksum = 0
            initial_header = struct.pack(
                "bbHHh", 8, 0, initial_checksum, id, 1)
            calculated_checksum = compute_checksum(initial_header)
            header = struct.pack("bbHHh", 8,
                                 0, calculated_checksum, id, 1)
            icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, time_to_live)
            icmp_socket.sendto(header, (dest_addr, 1))

            start_time = time.time()
            icmp_socket.settimeout(timeout)
            recv_packet, temp_addr = icmp_socket.recvfrom(1024)

            if recv_packet is not None:
                payload = recv_packet[IP_HEADER_SIZE:]
                if not verify_checksum(payload):
                    print(f'{"Checksum verification failed":<6}')
                icmp_header = recv_packet[20:28]
                type, code, checksum, p_id, sequence = struct.unpack('bbHHh', icmp_header)
                if p_id == id:
                    if (type, code)  in ICMP_ERRORS.items():
                        print(f'{ICMP_ERRORS[(type, code)]:<6}')
                    else:
                        if type != 0:
                            print(f'{"Unknown icmp error occured":<6}')
                ms = int((time.time() - start_time) * 1000.00)
                print(f'{str(ms) + "ms":<6}', end='\t')

            if temp_addr is not None:
                addr = temp_addr

        except socket.timeout:
            print(f'{"*":<6}', end='\t')

    if addr is not None:
        hostname = ''
        try:
            host_details = socket.gethostbyaddr(addr[0])
            if len(host_details) > 0:
                hostname = host_details[0]
        except Exception:
            hostname = 'Unknown host'
        print(f'{hostname}[{addr[0]}]')
        if addr[0] == dest_addr:
            return True
    else:
        print('Request timed out')
        return False
    return False


def traceroute(dest_host, requests_count, timeout):
    try:
        dest_addr = socket.gethostbyname(dest_host)
    except socket.gaierror:
        print("Invalid destination")
        return
    print(f"Tracert to {dest_addr} ({dest_host})")
    icmp_proto = socket.getprotobyname("icmp")
    try:
        for ttl in range(1, MAXTTL + 1):
            try:
                icmp_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_RAW, icmp_proto)
            except socket.error as e:
                print(f"Error {e}")
                return
            id = ttl
            if (ping(dest_addr, icmp_socket, ttl, id, timeout, requests_count)):
                icmp_socket.close()
                break
            icmp_socket.close()
        exit(0)
    except KeyboardInterrupt:
        print("\n[END] EXITING TRACE  ")
