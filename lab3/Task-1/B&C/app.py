import socket
from threading import Thread


def start_my_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('127.0.0.1', 2000))
        server.listen(4)
        print('Working...')
        while True:
            client_socket, address = server.accept()
            new_thread = Thread(target=on_new_client, args=(client_socket, address))
            new_thread.start()

    except KeyboardInterrupt:
        print(f'Gracefully shutting down the server')
    server.close()


def on_new_client(client_socket, connection):
    ip = connection[0]
    port = connection[1]
    print(f'THe new connection was made from IP: {ip}, and port: {port}!')
    data = client_socket.recv(1024).decode('utf-8')
    content = load_from_request(data)
    client_socket.send(content)
    client_socket.close()


def load_from_request(request_data):
    HDRS_200 = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    response = ''
    try:
        with open('views/' + request_data, 'rb') as file:
            response = file.read()
            print(response)
        return HDRS_200.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found').encode('utf-8')


if __name__ == '__main__':
    start_my_server()
