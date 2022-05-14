import socket
import PySimpleGUI as sg
from time import time

PACKET_SIZE = 1024
HOST = '127.0.0.1'
PORT = 8088


def create_tcp_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    return server_socket


def server_gui():
    window_configs = [
        [sg.Text('Введите IP', size=(20, 1)), sg.Text(HOST)],
        [sg.Text('Введите порт', size=(20, 1)), sg.Text(str(PORT))],
        [sg.Text('Пакетов получено:', size=(20, 1)), sg.Text(key='packets')],
        [sg.Text('Скорость передачи:', size=(20, 1)), sg.Text(key='speed')],
        [sg.Button('Начать получение данных')],
    ]

    return sg.Window('TCP Server', window_configs)


def receive_packets(server_socket, window):
    total_packets = 0
    packets_count = 0
    speed = 0
    first_msg_time = 0
    last_msg_time = 1

    while True:
        event, values = window.read(100)

        if event in (None, 'Exit'):
            break

        if event == 'Начать получение данных':
            packets_count = 0
            first_msg_time = 0

            try:
                recv_socket, _ = server_socket.accept()
                total_packets = int(recv_socket.recv(PACKET_SIZE).decode('utf-8'))
                for i in range(total_packets):
                    try:
                        cur_time = time()
                        recv_msg = recv_socket.recv(PACKET_SIZE).decode('utf-8')
                        if recv_msg != '':
                            packets_count += 1
                            if first_msg_time == 0:
                                first_msg_time = cur_time
                    except socket.timeout:
                        print('Request timed out')
                last_msg_time = time()
                recv_socket.close()
            except Exception as e:
                print(f'Error while packets receiving: {e}')

        total_time = (last_msg_time - first_msg_time) * 1000
        if total_time > 0:
            speed = round(PACKET_SIZE * packets_count / total_time)
        window['packets'].Update(f'{packets_count}/{total_packets}')
        window['speed'].Update(f'{speed} KB/s')

    server_socket.close()


if __name__ == '__main__':
    server_socket = create_tcp_socket()
    window = server_gui()
    receive_packets(server_socket, window)
