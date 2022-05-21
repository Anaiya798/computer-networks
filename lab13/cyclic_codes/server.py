from shared_functions import *

import socket


def server():
    s = socket.socket()
    print("Socket successfully created")
    port = PORT

    s.bind(('', port))
    s.listen(5)
    print("Socket is listening")

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        pkg_number = c.recv(1024).decode()
        for _ in range(int(pkg_number)):
            payload = c.recv(1024).decode()
            cyclic_code = c.recv(1024).decode()

            payload = (''.join(format(ord(x), 'b') for x in payload))
            if encode_data(payload, KEY) == cyclic_code:
                c.sendto('Correct'.encode(), (HOST, PORT))
            else:
                c.sendto('Error in data'.encode(), (HOST, PORT))

        c.close()


if __name__ == '__main__':
    server()
