from string import Template
from src.mail_sender import MailSender
import smtplib
import pandas as pd
from src.database_reader import customer_query
from argparse import ArgumentParser

import sys
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, "../../"))

# %% Mail


def open_smtp():
    # Open mail connection
    my_adress = "lucas.apap@incroyablelogiciel.com"
    smtpObj = smtplib.SMTP('localhost')
    # My credentials
    # from data.my_credentials import *
    # smtpObj = smtplib.SMTP(server_name, server_number)
    # smtpObj.starttls()
    # smtpObj.login(MY_ADDRESS, password)

    return my_adress, smtpObj


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# %% Database Query / Operations


def add_client(customer_database):
    # Modify client
    return 0


def main(args):

    # Get customers I want
    # customers = customer_query(software_skills=["Python"],
    #                           job="Ingénieur d'étude",
    #                           region="Ile-de-France")

    dict_args = vars(args)
    customers = customer_query(**dict_args)

    if len(customers) == 0:
        raise ValueError("No customer found")

    # Access Template Push
    msg_template = read_template('data/raw/push_message.txt')

    # Instanciate SMTP and mail sender
    my_adress, smtpObj = open_smtp()
    mail_sender = MailSender(my_adress, smtpObj)

    # For each contact, send the email:
    for customer in customers:
        msg_args = {
            "CUSTOMER_NAME": customer["name"].title(),
            "CUSTOMER_SURNAME": customer["surname"].title(),
            "CUSTOMER_JOB": customer["job"]
        }
        dest_mail = customer["mail"]
        mail_sender.send_mail(msg_template, msg_args, dest_mail)
    smtpObj.quit()

    return 0


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--job", dest='job', type=str,
                        default="Ingénieur d'étude", help='Which job ?')
    parser.add_argument("--region", dest='region', type=str,
                        default="Ile-de-France", help='Which region ?')

    # Parse
    args = parser.parse_args()
    #args = parser.parse_args(["--job=Ingénieur d'étude", "--region=Ile-de-France"])
    # e.g. :   args = parser.parse_args(["--job=Ingénieur d'étude", "--region=Ile-de-France"])

    # train
    main(args)
