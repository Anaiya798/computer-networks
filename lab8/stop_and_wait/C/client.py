import socket
from checksum import calc_checksum, verify_checksum
from random import uniform


def read_file(filename, chunk_size):
    try:
        file = open(filename, "rb")
        pkgs = []
        try:
            bytes_read = file.read(chunk_size)
            pkgs.append(bytes_read)
            while bytes_read:
                bytes_read = file.read(chunk_size)
                pkgs.append(bytes_read)
        except Exception:
            print(f'Unknown exception while reading from {filename}')
        finally:
            file.close()
        pkgs.append('END'.encode('utf-8'))
        return pkgs
    except FileNotFoundError:
        print(f'No such file or directory {filename}')


def process_data(data, type='general'):
    content_size = None
    if type == 'ack':
        data = data.split('\n')
        content_size = int(data[2].split(':')[1])
        checksum = int(data[3].split(':')[1])
        raw_data = '\n'.join(data[:3])
    else:
        data = data.split('\n\t\n')
        checksum = int(data[1].split(':')[1])
        raw_data = '\n'.join(data[:1])

    return content_size, checksum, raw_data


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
