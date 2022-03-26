import socket

from threading import Thread
from datetime import datetime
import time


def clients_listener(server, clients):
    while True:
        conn, address = server.recvfrom(1024)
        print(f'Connected with new client {address}')
        clients.append(address)


def server(host, port):
    print('Server running...')
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))
    clients = []
    new_clients_handler = Thread(target=clients_listener, args=[server, clients])
    new_clients_handler.start()
    while True:
        cur_time = str(datetime.now())
        time.sleep(1)
        for client in clients:
            server.sendto(cur_time.encode('utf-8'), client)


if __name__ == '__main__':
    host = input('Enter server host: ')
    port = int(input('Enter server port: '))
    server(host, port)
