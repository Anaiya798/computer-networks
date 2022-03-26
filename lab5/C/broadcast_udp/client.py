import socket


def client(server_host, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(b'Want connection', (server_host, server_port))
    while True:
        cur_time = client.recvfrom(1024)[0]
        print(cur_time.decode('utf-8'))


if __name__ == '__main__':
    server_host = input('Enter server host: ')
    server_port = int(input('Enter server port: '))
    client(server_host, server_port)
