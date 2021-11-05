from email import message
import mimetypes
import os
# from email.mime import multipart
# from email.mime import text
import smtplib

import config

class SendMail(object):
    def __init__(self):
        self._smtp_host = config.host
        self._smtp_port = config.port
        self._send_from = config.from_email
        self._username = config.username
        self._password = config.password

    def send_yahoo(self, subject, body, send_to, cc=None, bcc=None, files=[]):
        self._send_to = send_to

        msg = message.EmailMessage()
        #msg = multipart.MIMEMultipart()
        if 'cc' in locals():
            msg['Cc'] = cc
        if 'bcc' in locals():
            msg['Bcc'] = bcc
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self._send_from
        msg['To'] = self._send_to
        #msg.attach(text.MIMEText('Test email', 'plain'))

        for file in files:
            ctype, encoding = mimetypes.guess_type(file)
            if (ctype is None) or (encoding is not None):
                ctype = 'application/octret-stream'
            maintype, subtype = ctype.split('/', 1)
            with open(file, 'rb') as fp:
                msg.add_attachment(
                    fp.read(),
                    maintype = maintype,
                    subtype = subtype,
                    filename = os.path.basename(file)
                )

        server = smtplib.SMTP_SSL(self._smtp_host, self._smtp_port)
        server.ehlo()
#server.starttls()
#server.ehlo()
        server.login(self._username,self._password)
        server.send_message(msg)
        server.quit()
        print('send OK!!!')

yahoo_send_mail = SendMail()
yahoo_send_mail.send_yahoo('うん', 'はやく機種変しろ', 'uema.sa.m4@gmail.com', None, None, ['./test.txt'])
