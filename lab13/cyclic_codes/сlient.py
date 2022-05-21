from file_processing import read_file
from shared_functions import *

from random import uniform
import socket

CHUNK_SIZE = 5


def client():
    s = socket.socket()
    s.connect((HOST, PORT))

    file_data = read_file('alice', CHUNK_SIZE)
    s.sendto(str(len(file_data)).encode(), (HOST, PORT))
    for i in range(len(file_data)):
        cur_data = str(file_data[i])[2:-1]
        print(f'Package payload: {cur_data}')
        cur_data_binary = (''.join(format(ord(x), 'b') for x in cur_data))
        print(f'Binary encoded data: {cur_data_binary}')
        seed = uniform(0, 1)
        if seed > 0.9:
            cur_data_binary = cur_data_binary.replace('1', '0')
        cyclic_code = encode_data(cur_data_binary, KEY)
        print(f'Cyclic_code: {cyclic_code}')
        s.sendto(cur_data.encode(), (HOST, PORT))
        s.sendto(cyclic_code.encode(), (HOST, PORT))
        print(f'Received feedback from server: {s.recv(1024).decode()}\n')
    s.close()


if __name__ == '__main__':
    client()
