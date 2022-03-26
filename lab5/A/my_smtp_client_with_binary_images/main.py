import socket
import base64
import ssl

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587


def binary_image(img):
    with open(img, 'rb') as f:
        binary = base64.b64encode(f.read())
    return binary


img = binary_image('iphone11.png')


def smtp_client(email_from, password, email_to, subject, text, wanted_image):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((MAIL_SERVER, MAIL_PORT))

    connection_recv = client.recv(1024)
    print(f'Connection recv: {connection_recv}')

    hello_cmd = 'HELO Alice\r\n'.encode()
    client.send(hello_cmd)
    hello_recv = client.recv(1024)
    print(f'Hello recv: {hello_recv}')

    start_tls_cmd = "STARTTLS\r\n".encode()
    client.send(start_tls_cmd)
    tls_recv = client.recv(1024)
    print(f'TLS recv: {tls_recv}')

    ssl_client = ssl.wrap_socket(client)
    secret_email_from = base64.b64encode(email_from.encode())
    secret_password = base64.b64encode(password.encode())

    auth_cmd = "AUTH LOGIN\r\n"
    ssl_client.send(auth_cmd.encode())
    auth_recv = ssl_client.recv(1024)
    print(f'AUTH recv: {auth_recv}')

    ssl_client.send(secret_email_from + "\r\n".encode())
    mail_encrypted_recv = ssl_client.recv(1024)
    print(f'Mail encrypted recv: {mail_encrypted_recv}')

    ssl_client.send(secret_password + "\r\n".encode())
    password_encrypted_recv = ssl_client.recv(1024)
    print(f'Password encrypted recv: {password_encrypted_recv}')

    mail_from = "MAIL FROM: <{}>\r\n".format(email_from)
    ssl_client.send(mail_from.encode())
    mail_from_recv = ssl_client.recv(1024)
    print(f'Mail from recv: {mail_from_recv}')

    mail_to = "RCPT TO: <{}>\r\n".format(email_to)
    ssl_client.send(mail_to.encode())
    mail_to_recv = ssl_client.recv(1024)
    print(f'Mail from recv: {mail_to_recv}')

    data = 'DATA\r\n'
    ssl_client.send(data.encode())
    data_recv = ssl_client.recv(1024)
    print(f'Data recv: {data_recv}')

    msg = '{}. \r\n'.format(text)
    end_msg = '\r\n.\r\n'
    if wanted_image == 'yes':
        ssl_client.send("Subject: {}\n\n{}\n{}".format(subject, msg, str(img)).encode())
    else:
        ssl_client.send("Subject: {}\n\n{}".format(subject, msg).encode())
    ssl_client.send(end_msg.encode())
    msg_recv = ssl_client.recv(1024)
    print(f'Msg recv: {msg_recv}')

    quit_cmd = 'QUIT\r\n'
    ssl_client.send(quit_cmd.encode())
    quit_recv = ssl_client.recv(1024)
    print(f'Msg recv: {quit_recv}')

    ssl_client.close()
    print('Done!')


if __name__ == '__main__':
    email_from = input("Enter sender email: ")
    password = input("Enter password: ")
    email_to = input("Enter receiver email: ")
    subject = input("Enter subject of the email: ")
    text = input("Enter email text: ")
    wanted_image = input("Add binary image(yes/no): ")
    smtp_client(email_from, password, email_to, subject, text, wanted_image)
