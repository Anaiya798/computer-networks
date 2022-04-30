from help_functions import read_file

import socket
import time

HOST = socket.gethostname()
IP = socket.gethostbyname(HOST)
PORT = 1234
SLIDING_WINDOW = 2
CHUNK_SIZE = 100


def calc_statistics(acc_packets, total_packets_number, position_start, position_end):
    print(f'Packets {acc_packets[0]} - {acc_packets[len(acc_packets) - 1]} already got ACK')
    print(f'The sliding window is in the range {position_start} - {position_end}')
    print(f'Packets {position_end + 1} - {total_packets_number} have not been transmitted yet')


if __name__ == '__main__':

    client = socket.socket()
    print("\nTrying to connect to ", HOST, "(", PORT, ")\n")
    time.sleep(1)
    client.connect((HOST, PORT))
    print("connected...\n")

    packets = read_file('alice.txt', CHUNK_SIZE)

    while True:
        message_length = str(len(packets))
        client.send(message_length.encode())
        i = 0
        SLIDING_WINDOW -= 1
        message_length = int(message_length)
        k = SLIDING_WINDOW

        while i != message_length:
            acc_packets = []
            while (i != (message_length - SLIDING_WINDOW)):
                client.send(packets[i])
                ans = client.recv(1024)
                ans = ans.decode()
                if (ans != "ACK Lost"):
                    time.sleep(1)
                    print(ans)
                    print('Acknowledgement Received!')
                    acc_packets.append(i)
                    i = i + 1
                    k = k + 1
                    calc_statistics(acc_packets, message_length, i, k)
                    print('Now sending the next packet')
                    print('====')
                    print('\n')
                    time.sleep(1)
                else:
                    time.sleep(1)
                    print(ans)
                    print('Acknowledgement of the data bit is LOST!')
                    calc_statistics(acc_packets, message_length, i + 1, k + 1)
                    print('Now resending the same packet')
                    print('====')
                    print('\n')
                    time.sleep(1)
            while (i != message_length):
                client.send(packets[i])
                ans = client.recv(1024)
                ans = ans.decode()
                if (ans != "ACK Lost"):
                    time.sleep(1)
                    print(ans)
                    print('Acknowledgement Received!')
                    acc_packets.append(i)
                    i = i + 1
                    print(i)
                    calc_statistics(acc_packets, message_length, i, k)
                    print('Now sending the next packet')
                    print('====')
                    print('\n')
                    time.sleep(1)
                else:
                    time.sleep(1)
                    print(ans)
                    print('Acknowledgement of the data bit is LOST!')
                    calc_statistics(acc_packets, message_length, i + 1, k)
                    print('Now resending the same packet')
                    print('====')
                    print('\n')
                    time.sleep(1)
        print('Transmitting finished!')
