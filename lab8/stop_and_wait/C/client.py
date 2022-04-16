import socket
from checksum import calc_checksum, verify_checksum
from random import uniform
from shared_functions import process_data, read_file


def get_answer(client):
    data = client.recvfrom(1024)[0]
    data = data.decode('utf-8')
    if data[:5] != 'PKG_0' and data[:5] != 'PKG_1' and 'CONTENT SIZE' and 'CHECKSUM' not in data:
        raise Exception
    print(data)
    print('====')
    print()

    content_size, checksum, raw_data = process_data(data, 'ack')
    if not verify_checksum(checksum.to_bytes(2, byteorder='big') + raw_data.encode('utf-8')):
        raise Exception
    if content_size > 0:
        receive_file(client, content_size)


def receive_file(client, content_size):
    for i in range(content_size):
        try:
            data = client.recvfrom(1024)[0]
            data = data.decode('utf-8')
            _, checksum, raw_data = process_data(data)
            if not verify_checksum(checksum.to_bytes(2, byteorder='big') + raw_data.encode('utf-8')):
                raise Exception
            try:
                with open('server_statistics.txt', 'a') as f:
                    f.write(raw_data)
            except Exception:
                print('Unknown error while writing to file: server_statistics.txt')
        except Exception:
            print('Request timed out. Package was lost on server!')


def client(pkgs, timeout):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect(('127.0.0.1', 2000))
    client.settimeout(timeout)

    for i in range(len(pkgs)):
        loss_threshold = uniform(0, 1)
        if loss_threshold > 0.7:
            print(f'Package {i} was lost on client')
            print()
            continue
        else:
            print('====')
            print(f'Sending package {i}')
            header_number = 'PKG_0\r\n'
            msg = header_number.encode('utf-8') + pkgs[i]
            checksum = str(calc_checksum(msg))
            client.sendto((msg.decode('utf-8') + '\n\t\nCHECKSUM: ' + checksum).encode('utf-8'),
                          ('127.0.0.1', 2000))
            try:
                get_answer(client)
            except Exception:
                print('Request timed out. Sending one more time...')
                header_number = 'PKG_1\r\n'
                msg = header_number.encode('utf-8') + pkgs[i]
                checksum = str(calc_checksum(msg))
                client.sendto((msg.decode('utf-8') + '\n\t\nCHECKSUM: ' + checksum).encode('utf-8'),
                              ('127.0.0.1', 2000))
                try:
                    get_answer(client)
                except Exception:
                    print('Request timed out. Package was lost on server!')
                    print('====')
                    print()


if __name__ == '__main__':
    filename = input('File to send: ')
    chunk_size = int(input('Number of bytes in one package: '))
    timeout = int(input('Max time for waiting answer from server (seconds): '))
    pkgs = read_file(filename, chunk_size)
    pkgs.append('statistics'.encode('utf-8'))
    client(pkgs, timeout)
