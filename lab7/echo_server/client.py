import socket
from datetime import datetime
from time import time


def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(('127.0.0.1', 2000))
    client.settimeout(1)

    for i in range(1, 11):
        msg = f'Ping {i} {datetime.now()}'
        start = time()
        client.sendto(msg.encode('utf-8'), ('127.0.0.1', 2000))
        try:
            data = client.recvfrom(1024)[0].decode('utf-8')
            rtt = time() - start
            print(data)
            print(f'RTT: {rtt} seconds')
            print('============')
        except Exception:
            print('Request timed out\n')


if __name__ == '__main__':
    client()



