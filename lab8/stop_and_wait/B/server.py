import socket
from datetime import datetime
from random import uniform
from shared_functions import read_file


ACK = 'The server received your package'
CHUNK_SIZE = 100


def send_file(server, addr, pkgs):
    for i in range(len(pkgs)):
        loss_threshold = uniform(0, 1)
        if loss_threshold > 0.7:
            continue
        try:
            server.sendto(pkgs[i], addr)
        except Exception:
            print('Connection lost')


def add_statistics(data):
    try:
        with open('statistics.txt', 'a') as f:
            f.write('====\n')
            f.write(f'{datetime.now()}\n')
            f.write(f'Received {len(data.encode("utf-8"))} bytes\n')
            f.write(f'Decoded data: {data}\n')
            f.write('====\n')
            f.write('\n\n')
    except Exception:
        print('Unknown error while writing to file: statistics.txt')


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 2000))
    print('Server running...')
    try:
        while True:
            content_size = 0
            pkgs = []
            acc_files_counter = 1

            data, addr = server.recvfrom(1024)
            if not data:
                continue
            data = data.decode('utf-8')
            loss_threshold = uniform(0, 1)
            if loss_threshold > 0.7:
                continue
            elif data[:5] != 'PKG_0' and data[:5] != 'PKG_1':
                continue
            else:
                if data[7:] == 'statistics':
                    pkgs = read_file('statistics.txt', CHUNK_SIZE)
                    content_size = len(pkgs)

                ack_msg = data[:5] + '\n' + ACK + '\nCONTENT SIZE: ' + str(content_size)
                server.sendto(ack_msg.encode('utf-8'), addr)

                if content_size > 0:
                    send_file(server, addr, pkgs)

                add_statistics(data)

                if data[7:] == 'END':
                    acc_files_counter += 1
                    continue

                filename = 'decoded_file_' + str(acc_files_counter) + '.txt'
                try:
                    with open(filename, 'a') as f:
                        f.write(data[7:])
                except Exception:
                    print(f'Unknown error while writing to file: {filename}')

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server()
