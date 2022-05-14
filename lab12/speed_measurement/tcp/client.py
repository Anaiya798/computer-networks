import socket
import datetime
import PySimpleGUI as sg
from random import choice, uniform
from string import ascii_letters

PACKET_SIZE = 1024


def create_message(length):
    return ''.join(choice(ascii_letters) for _ in range(length))


def client_gui():
    window_configs = [
        [sg.Text('IP-адрес получателя: ', size=(20, 1)), sg.InputText('127.0.0.1', key='host')],
        [sg.Text('Порт получателя: ', size=(20, 1)), sg.InputText('8088', key='port')],
        [sg.Text('Количество пакетов: ', size=(20, 1)), sg.InputText('5', key='packets')],
        [sg.Button('Отправить пакеты')],
    ]
    return sg.Window('TCP Client', window_configs)


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


def send_packets(window):
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
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, port))
                client_socket.sendall(bytes(str(packets_number), encoding='utf-8'))
                for i in range(packets_number):
                    cur_time = datetime.datetime.now()
                    msg = str(cur_time) + ' ' + create_message(PACKET_SIZE - len(str(cur_time)))
                    seed = uniform(0, 1)
                    if seed < 0.9:  # моделируем 10%-ую потерю
                        client_socket.sendall(msg.encode('utf-8'))
                client_socket.close()
            except Exception as e:
                print(f'Sending packets failed: {e}')


if __name__ == '__main__':
    window = client_gui()
    send_packets(window)
