import socket
from random import uniform

ACK = 'The server received your package'


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        server.bind(('127.0.0.1', 2000))
        print('Server running...')
        while True:
            data, addr = server.recvfrom(1024)
            data = data.decode('utf-8')
            loss_threshold = uniform(0, 1)
            if loss_threshold > 0.7:
                continue
            else:
                if data[:5] != 'PKG_0' and data[:5] != 'PKG_1':
                    msg = 'Invalid package format: header PKG_NUMBER missing. Ignored'
                    server.sendto(msg.encode('utf-8'), addr)
                else:
                    msg = data[:5] + ' ' + ACK
                    server.sendto(msg.encode('utf-8'), addr)
                    try:
                        with open('decoded_file.txt', 'a') as f:
                            f.write(data[7:])
                    except Exception:
                        print('Unknown error while writing')

    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server()
