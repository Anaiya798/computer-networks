import time
import socket
from random import uniform

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 1234
SLIDING_WINDOW = 5

if __name__ == '__main__':
    time.sleep(1)

    server = socket.socket()
    print('Server running...')
    time.sleep(1)

    server.bind((HOST, PORT))
    server.listen(4)

    conn, addr = server.accept()
    print("Received serverection from ", addr[0], "(", addr[1], ")\n")

    while True:
        message_length = conn.recv(1024)
        message_length = int(message_length.decode())
        i = 0
        while i != message_length:
            loss_threshold = uniform(0, 1)
            if loss_threshold > 0.8:
                ans = "ACK Lost"
                message = conn.recv(1024)
                message = message.decode()
                conn.send(ans.encode())

            else:
                ans = "ACK " + str(i)
                message = conn.recv(1024)
                message = message.decode()

                conn.send(ans.encode())
                i = i + 1

