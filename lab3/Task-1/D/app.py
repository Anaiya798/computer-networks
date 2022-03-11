import socket
from multiprocessing import Pool


def start_my_server(concurrency_level):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    pool = Pool(processes=10)
    process_count = 0
    process_number = 1
    processes = []
    queue = []
    waiting = False

    try:
        server.bind(('127.0.0.1', 2000))
        server.listen(10)
        print('Working...')
        while True:
            client_socket, address = server.accept()
            queue.append((client_socket, address))
            print(f'queue update, process added: {queue}')

            while queue != []:
                for process in processes:
                    if process[1].ready():
                        print(f'ended process: {process}')
                        print('Server is free!')
                        process_count -= 1
                        processes.remove(process)
                if process_count < concurrency_level:
                    waiting = False
                    print(f'process_count: {process_count}')
                    new_process = pool.apply_async(on_new_client, queue[0])
                    processes.append((process_number, new_process))
                    process_count += 1
                    process_number += 1
                    print('New process has started')
                    print(f'new_process: {new_process}')
                    print(f'process_count: {process_count}')
                    queue.remove(queue[0])
                    print(f'queue: {queue}')
                else:
                    if not waiting:
                        print(process_count)
                        print('Server is busy, wait...')
                        waiting = True

    except KeyboardInterrupt:
        print(f'Gracefully shutting down the server')
    server.close()


def on_new_client(client_socket, connection):
    ip = connection[0]
    port = connection[1]
    i = 0
    while i < 100000000:  # цикл нужен для демонстрации того, что процессы создаются, как надо
        i += 1
    print(f'THe new connection was ma'
          f'de from IP: {ip}, and port: {port}!')
    data = client_socket.recv(1024).decode('utf-8')
    content = load_from_request(data)
    client_socket.send(content)
    client_socket.close()


def load_from_request(request_data):
    HDRS_200 = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    response = ''
    try:
        with open('views/' + request_data, 'rb') as file:
            response = file.read()
        return HDRS_200.encode('utf-8') + response
    except FileNotFoundError:
        return (HDRS_404 + 'Page not found').encode('utf-8')


if __name__ == '__main__':
    concurrency_level = int(input('Enter the server concurrency level:'))
    start_my_server(concurrency_level)
