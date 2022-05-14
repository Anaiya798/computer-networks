import socket
import datetime
import PySimpleGUI as sg
from random import choice, uniform
from string import ascii_letters

PACKET_SIZE = 1024
HOST = '127.0.0.1'
PORT = 8088


def create_message(length):
    return ''.join(choice(ascii_letters) for _ in range(length))


def client_gui():
    window_configs = [
        [sg.Text('IP-адрес получателя: ', size=(20, 1)), sg.InputText(HOST, key='host')],
        [sg.Text('Порт получателя: ', size=(20, 1)), sg.InputText(PORT, key='port')],
        [sg.Text('Количество пакетов: ', size=(20, 1)), sg.InputText('5', key='packets')],
        [sg.Button('Отправить пакеты')],
    ]
    return sg.Window('UDP Client', window_configs)


def create_udp_socket():
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_udp_socket.settimeout(1)
    return client_udp_socket


def host_check(host):
    if '.' not in host:
        return False
    host = [int(i) for i in host.split('.')]
    if len(host) != 4:
        return False
    for i in range(4):
        if host[i] < 0 or host[i] > 255:
            return False
    return True


def send_packets(client_udp_socket, window):
    while True:
        event, values = window.read()

        if event in (None, 'Exit'):
            break

        if event == 'Отправить пакеты':
            try:
                host, port = values['host'], int(values['port'])
                packets_number = int(values['packets'])
                if not host_check(host):
                    print('Invalid host')
            except ValueError:
                print('Port and packets number should be non-negative integers')
            except Exception as e:
                print(f'Parsing unput failed: {e}')

            try:
                client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_tcp_socket.connect((host, port))
                client_tcp_socket.sendall(bytes(str(packets_number), encoding='utf-8'))
                client_tcp_socket.close()
            except Exception as e:
                print(f'Sending the number of packets using TCP failed: {e}')

            try:
                for i in range(packets_number):
                    cur_time = datetime.datetime.now()
                    msg = f'{cur_time} '
                    msg += create_message(PACKET_SIZE - len(msg))
                    seed = uniform(0, 1)
                    if seed < 0.9:  # моделируем 10%-ую потерю
                        client_udp_socket.sendto(msg.encode('utf-8'), (host, port))
            except Exception as e:
                print(f'Sending packets failed: {e}')

    client_udp_socket.close()


if __name__ == '__main__':
    client_udp_socket = create_udp_socket()
    window = client_gui()
    send_packets(client_udp_socket, window)

