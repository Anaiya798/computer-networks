import socket

HOST = 'localhost'
PORT = 8088


def server():
    try:
        server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
    except Exception:
        print('Cannot start server')
        return
    print('Server running...')
    while True:
        client_request, address = server_socket.recvfrom(1024)
        client_request = client_request.decode('utf-8')
        print(f'Client request: {client_request}')

        response = client_request.upper().encode('utf-8')
        server_socket.sendto(response, address)
        print(f'Server: {response}')


if __name__ == '__main__':
    server()
