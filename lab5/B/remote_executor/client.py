import socket


def client(server_host, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))

    command = input('Enter command: ')
    client.sendall(command.encode('utf-8'))


if __name__ == '__main__':
    server_host = input('Enter server host: ')
    server_port = int(input('Enter server port: '))
    client(server_host, server_port)

