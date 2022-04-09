import socket
import time
from random import uniform


def start_my_server():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(('127.0.0.1', 2000))
        print('Server running...')
        while True:
            data, addr = server.recvfrom(1024)
            pause = uniform(0, 1)
            if pause > 0.8:
                continue
            else:
                time.sleep(pause)  # случайная задержка, чтобы RTT не было везде 0
                server.sendto(data.decode('utf-8').upper().encode('utf-8'), addr)

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    start_my_server()
