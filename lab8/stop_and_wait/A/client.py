import socket
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
        print('No such file or directory')


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
                data = client.recvfrom(1024)[0].decode('utf-8')
                print(data, i)
                print('====')
                print()

            except Exception:
                print('Request timed out. Sending one more time...')
                header_number = 'PKG_1\r\n'
                msg = header_number.encode('utf-8') + pkgs[i]
                client.sendto(msg, ('127.0.0.1', 2000))
                try:
                    data = client.recvfrom(1024)[0].decode('utf-8')
                    print(data, i)
                    print('====')
                    print()
                except Exception:
                    print('Request timed out. Package was lost on server!')
                    print('====')
                    print()


if __name__ == '__main__':
    filename = input('File to send: ')
    chunk_size = int(input('Number of bytes in one package: '))
    timeout = int(input('Max time for waiting answer from server (seconds): '))
    pkgs = read_file(filename, chunk_size)
    client(pkgs, timeout)
