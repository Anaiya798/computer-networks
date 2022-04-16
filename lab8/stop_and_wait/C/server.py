import socket

from checksum import calc_checksum, verify_checksum
from datetime import datetime
from random import uniform
from shared_functions import process_data, read_file

ACK = 'The server received your package'
CHUNK_SIZE = 100


def send_file(server, addr, pkgs):
    for i in range(len(pkgs)):
        loss_threshold = uniform(0, 1)
        if loss_threshold > 0.7:
            continue
        checksum = str(calc_checksum(pkgs[i]))
        server.sendto((pkgs[i].decode('utf-8') + '\n\t\nCHECKSUM: ' + checksum).encode('utf-8'), addr)


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
            elif data[:5] != 'PKG_0' and data[:5] != 'PKG_1' and 'CHECKSUM' not in data:
                continue

            else:
                _, checksum, raw_data = process_data(data)
                if not verify_checksum(checksum.to_bytes(2, byteorder='big') + raw_data.encode('utf-8')):
                    raise Exception

                if raw_data[7:] == 'statistics':
                    pkgs = read_file('statistics.txt', CHUNK_SIZE)
                    content_size = len(pkgs)

                ack_msg = raw_data[:5] + '\n' + ACK + '\nCONTENT SIZE: ' + str(content_size)
                checksum = str(calc_checksum(ack_msg.encode('utf-8')))
                server.sendto((ack_msg + '\nCHECKSUM: ' + checksum).encode('utf-8'), addr)

                if content_size > 0:
                    send_file(server, addr, pkgs)

                add_statistics(data)

                if raw_data[7:] == 'END':
                    acc_files_counter += 1
                    continue

                filename = 'decoded_file_' + str(acc_files_counter) + '.txt'
                try:
                    with open(filename, 'a') as f:
                        f.write(raw_data[7:])
                except Exception:
                    print(f'Unknown error while writing to file: {filename}')

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server()
