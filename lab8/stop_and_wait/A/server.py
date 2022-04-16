import socket
from random import uniform

ACK = 'The server received your package'


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 2000))
    print('Server running...')
    try:
        while True:
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

                ack_msg = data[:5] + '\n' + ACK
                server.sendto(ack_msg.encode('utf-8'), addr)

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
