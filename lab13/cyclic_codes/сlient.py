from file_processing import read_file
from shared_functions import *

from random import uniform
import socket


def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

        return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)
    tmp = divident[0: pick]
    while pick < len(divident):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0' * pick, tmp) + divident[pick]
        pick += 1
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword


def encode_data(data, key):
    l_key = len(key)

    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)

    codeword = data + remainder
    return codeword


if __name__ == '__main__':
    s = socket.socket()
    port = 12345
    s.connect(('127.0.0.1', port))

    file_data = read_file('alice', 5)
    s.sendto(str(len(file_data)).encode(), ('127.0.0.1', 12345))
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
        s.sendto(cur_data.encode(), ('127.0.0.1', 12345))
        s.sendto(cyclic_code.encode(), ('127.0.0.1', 12345))
        print(f'Received feedback from server: {s.recv(1024).decode()}\n')

    s.close()
