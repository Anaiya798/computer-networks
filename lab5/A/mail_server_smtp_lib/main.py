import os
import smtplib
from email.message import EmailMessage

with open('security.txt') as f:
    SENDER_ADDRESS = f.readline().strip()
    PASSWORD = f.readline().strip()


def send_email_message(receiver_address, type, subject, body):
    msg = EmailMessage()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver_address
    msg['Subject'] = subject
    if type == 'text':
        msg.set_content(body)
    else:
        msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                <p style="color:SlateGray;">{text}</p>
            </body>
        </html>
        """.format(text=body), subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_ADDRESS, PASSWORD)
        smtp.send_message(msg)
        print('Done!')


if __name__ == '__main__':
    receiver_address = input('Enter receiver email: ')
    type = input('Enter message type(text/html): ')
    if type != 'text' or type != 'html':
        print('Sorry, our server works only with text/html messages')
    else:
        subject = input('Enter subject of your message: ')
        body = input('Enter text of your message: ')
        send_email_message(receiver_address, type, subject, body)
