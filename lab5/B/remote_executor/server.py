import socket

from os import system


def server(host, port):
    print('Server running...')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(4)

    conn, address = server.accept()
    command = conn.recv(1024).decode('utf-8')
    print(f'Connected with client {address} and received command {command}')
    system(command)
    conn.close()


if __name__ == '__main__':
    host = input('Enter server host: ')
    port = int(input('Enter server port: '))
    server(host, port)
