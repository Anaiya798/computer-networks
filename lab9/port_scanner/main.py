import socket


def opened_ports(host, port_start, port_end):
    with open('opened_ports.txt', 'a') as f:
        f.write('Available ports: \n')
        f.close()

    opened_ports_count = 0

    for port in range(port_start, port_end + 1):
        try:
            s = socket.socket()
            s.settimeout(1)
            conn_res = s.connect_ex((host, port))
            if conn_res == 0:
                opened_ports_count += 1
                with open('opened_ports.txt', 'a') as f:
                    f.write(f'{port} \n')
                    f.close()
            s.close()
        except socket.error:
            print("Can't access the server")

    if opened_ports_count == 0:
        with open('opened_ports.txt', 'a') as f:
            f.write(f'No ports are available! \n')
            f.close()


if __name__ == '__main__':
    host = input('Enter host name: ')
    port_start = int(input('Enter start number of ports range: '))
    port_end = int(input('Enter end number of ports range: '))
    opened_ports(host, port_start, port_end)
