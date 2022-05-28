import smtplib
from email.message import EmailMessage

SENDER_ADDRESS = 'persikk3000@gmail.com'
PASSWORD = 'burningheartA2020'
TEXT = 'Рады видеть Вас в нашем сервисе вновь!'


def send_email_message(receiver_address):
    msg = EmailMessage()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver_address
    msg['Subject'] = 'greeting'
    msg.set_content(TEXT)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_ADDRESS, PASSWORD)
        smtp.send_message(msg)
        print('Done!')


if __name__ == '__main__':
    send_email_message('persikk3000@gmail.com')
