import socket
import argparse
import time

parser = argparse.ArgumentParser(description='This is a client for my server')
parser.add_argument('--host', metavar='host', type=str, nargs='?', default=socket.gethostname())
parser.add_argument('--port', metavar='port', type=int, nargs='?', default=2000)
parser.add_argument('--filename', metavar='filename', type=str, nargs='?', default=None)
parser.add_argument('--client-number', metavar='client_number', type=str, nargs='?', default=1)
args = parser.parse_args()

print(f'Connecting to server: {args.host} on port: {args.port}')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((args.host, args.port))
    print('Success')
except Exception as e:
    print(f'Failed to connect to host: {args.host} on port: {args.port}, because of: {e}')

file = open('server_answers' + args.client_number, 'w')
client.send(args.filename.encode('utf-8'))
start = time.time()
file.write(f'Start: {start}\n\n')
data = client.recv(1024)
end = time.time()
file.write(f"The server's response was:\n {data.decode('utf-8')}\n\n")
file.write(f'End: {end}')
