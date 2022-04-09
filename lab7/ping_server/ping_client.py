import socket
from datetime import datetime
from time import time


def calc_statistics(pkgs, data, rtts):
    rtts_length = len(rtts)
    print('=========')
    print(f'Received data: {data}')
    print()
    print('Total:')
    print(f'{pkgs} packages were transmitted, {rtts_length} answers were receieved')
    print(f'Package loss: {round((1 - rtts_length / pkgs) * 100, 2)} %')
    print(f'Min RTT: {round(min(rtts) * 1000, 2)} ms')
    print(f'Max RTT: {round(max(rtts) * 1000, 2)} ms')
    print(f'Average RTT: {round(sum(rtts) / rtts_length * 1000, 2)}')
    print('=========')
    print()


def client(pkgs_number, timeout):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(('127.0.0.1', 2000))
    client.settimeout(timeout)

    rtts = []
    for i in range(1, pkgs_number + 1):
        msg = f'Ping {i} {datetime.now()}'
        start = time()
        client.sendto(msg.encode('utf-8'), ('127.0.0.1', 2000))
        try:
            data = client.recvfrom(1024)[0].decode('utf-8')
            rtt = time() - start
            rtts.append(rtt)
            calc_statistics(i, data, rtts)
        except Exception:
            print('Request timed out\n')


if __name__ == '__main__':
    pkgs_number = int(input('Enter the number of packages you want to send: '))
    timeout = int(input('Enter max waiting time (seconds): '))
    client(pkgs_number, timeout)
