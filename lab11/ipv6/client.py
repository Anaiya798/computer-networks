import socket

HOST = 'localhost'
PORT = 8088
TIMEOUT = 1


def client():
    try:
        client_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.settimeout(TIMEOUT)
    except Exception:
        print('Cannot run client')
        return

    msg = 'Hello'
    client_socket.sendto(msg.encode('utf-8'), (HOST, PORT))
    print(f'Client message: {msg}')

    try:
        response, _ = client_socket.recvfrom(1024)
        response = response.decode('utf-8')
        print(f'Server response: {response}')
    except socket.timeout:
        print(f'Request timed out\n')


if __name__ == '__main__':
    client()
