import socket
from random import uniform
from shared_functions import read_file


def get_content_size(data):
    data = data.split('\n')
    content_size = int(data[2].split(':')[1])
    return content_size


def receive_file(client, content_size):
    for i in range(content_size):
        try:
            data = client.recvfrom(1024)[0]
            data = data.decode('utf-8')
            try:
                with open('server_statistics.txt', 'a') as f:
                    f.write(data)
            except Exception:
                print('Unknown error while writing to file: server_statistics.txt')
        except Exception:
            print('Request timed out. Package was lost on server!')


def get_answer(client):
    data = client.recvfrom(1024)[0].decode('utf-8')

    if data[:5] != 'PKG_0' and data[:5] != 'PKG_1' and 'CONTENT SIZE' not in data:
        raise Exception

    print(data)
    print('====')
    print()

    content_size = get_content_size(data)
    if content_size > 0:
        receive_file(client, content_size)


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
            client.sendto(msg, ('127.0.0.1', 2000))
            try:
                get_answer(client)
            except Exception:
                print('Request timed out. Sending one more time...')
                header_number = 'PKG_1\r\n'
                msg = header_number.encode('utf-8') + pkgs[i]
                client.sendto(msg, ('127.0.0.1', 2000))
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
