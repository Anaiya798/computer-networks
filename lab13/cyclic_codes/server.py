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
    print("socket binded to %s" % (port))
    s.listen(5)
    print("socket is listening")

    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        input_string = c.recv(1024).decode()
        input_string = (''.join(format(ord(x), 'b') for x in input_string))
        data = c.recv(1024)

        print("Received encoded data in binary format :", data.decode())

        if not data:
            break

        key = "1001"
        if encode_data(input_string, key) == data.decode():
            c.sendto('Correct'.encode(), ('127.0.0.1', 12345))
        else:
            c.sendto('Error in data'.encode(), ('127.0.0.1', 12345))

        c.close()
