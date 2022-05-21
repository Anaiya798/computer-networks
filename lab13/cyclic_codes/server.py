from shared_functions import *

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
    print("Socket successfully created")
    port = 12345

    s.bind(('', port))
    s.listen(5)
    print("Socket is listening")

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        pkg_number = c.recv(1024).decode()
        for _ in range(int(pkg_number)):
            payload = c.recv(1024).decode()
            cyclic_code = c.recv(1024).decode()

            payload = (''.join(format(ord(x), 'b') for x in payload))
            if encode_data(payload, KEY) == cyclic_code:
                c.sendto('Correct'.encode(), ('127.0.0.1', 12345))
            else:
                c.sendto('Error in data'.encode(), ('127.0.0.1', 12345))

        c.close()
