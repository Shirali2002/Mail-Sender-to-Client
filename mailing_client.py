# This is a mail sender program.
# To use this program, firstly we have to disabling 2-step verification and allow less secure apps
# Step1 [Link of Disabling 2-step verification]:
# https://myaccount.google.com/security?utm_source=OGB&utm_medium=act#signin
# Step 2 [Link for Allowing less secure apps]:
# https://myaccount.google.com/u/1/lesssecureapps?pli=1&pageId=none
# Then we can run this program.
# Program will direct us to functions.

import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


def file_attacher(file_path, msg):
    filename = file_path
    attachment = open(filename, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())

    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f'attachment: filename={filename}')
    msg.attach(p)

    return msg


def mail_sender(sender_login, sender_password, receiver, subject, message_path, file_path=None):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login(sender_login, sender_password)

    msg = MIMEMultipart()
    msg['From'] = sender_login
    msg['To'] = receiver
    msg['Subject'] = subject

    with open(message_path, 'r') as file:
        message = file.read()

    msg.attach(MIMEText(message, 'plain'))

    if file_path != '':
        msg = file_attacher(file_path=file_path, msg=msg)

    text = msg.as_string()
    server.sendmail(sender_login, receiver, text)

    server.quit()

    print('Mail sent successfully.')


if __name__ == '__main__':
    while True:
        print('''
            (1) sending email
            (2) add receiver to receiver list
            (3) exit
        ''')
        secim = int(input('Enter your choice: '))

        if secim == 1:
            sender_login = input('Enter username of the sender gmail.(ex. username@gmail.com)\n')
            sender_password = input('Enter the sender gmail password.\n')
            receiver_file = input('Enter path of the receiver list.\n')
            subject = input('Enter the subject of the email.\n')
            message_path = input('Enter the path to the message file.\n')
            file_path = input('If you want to add file, write the path of the file. If not press enter.\n')
            with open(receiver_file, 'r') as file:
                receiver_list = file.read().split('\n')
                receiver_list.pop(len(receiver_list)-1)

            count = 0
            while count < len(receiver_list):
                receiver_username = receiver_list[count]
                mail_sender(sender_login=sender_login, sender_password=sender_password, receiver=receiver_username, subject=subject, message_path=message_path, file_path=file_path)
                count += 1
        elif secim == 2:
            receiver = ''
            while receiver != 'quit':
                receiver = input('Enter receiver username. If you added all elements, enter "quit" to continue\n')
                if receiver != 'quit':
                    with open('receiver_list.txt', 'a') as file:
                        file.write(receiver+'\n')
        elif secim == 3:
            quit()
