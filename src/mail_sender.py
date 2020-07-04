# TODO checker

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror


class MailSender():

    def __init__(self, my_mail, smtpObj):
        self.my_mail = my_mail
        self.smtpObj = smtpObj

    def send_mail(self, msg_template, msg_args, dest_mail):
        msg = MIMEMultipart()  # create a message

        # add in the actual person name to the message template
        message = msg_template.substitute(**msg_args)

        # setup the parameters of the message
        msg['From'] = self.my_mail
        msg['To'] = dest_mail
        msg['Subject'] = "Push de candidat - {}".format(msg_args["CUSTOMER_JOB"])

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        try:
            self.smtpObj.send_message(msg)
        except (gaierror, ConnectionRefusedError):
            # tell the script to report if your message was sent or which errors need to be fixed
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
        else:
            print('Sent')