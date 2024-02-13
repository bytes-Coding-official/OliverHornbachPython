# Description: This script reads a file and extracts the email addresses and the subject from the file.

# infos through chatgpt: https://chat.openai.com/share/06a411b9-976e-4167-b5c8-8696f79c9241

import re
# imports
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

mails_dict = dict()

with open("liste.txt", "r") as file:
    for line in file:
        emails = []
        extensions = []
        # get the subject from the line that is in between ""
        try:
            subject = re.search('\"(.+?)\"', line).group(1)
            # get the emails from the line
            # the emails are ending with @hornbach.com and than a whitespace as a seperator
            mails = re.findall(r'[\w\.-]+@hornbach.com', line)
            # save all extensions that are after the "-a" tag
            # the extensions are ending with a whitespace as a seperator e.g. 
            extensions = re.findall(r'-a (.+?) ', line)
            # add every single email to the list
            for mail in mails:
                emails.append(mail)
            # add the emails to the dictionary with the subject as the key
            mails_dict[subject] = (emails, extensions)
        except AttributeError:
            pass

for key, value in mails_dict.items():
    print(key, ":", value)
    print()

# Email credentials
smtp_host = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'verteiler@deinemail.de'
smtp_password = 'password'


def send_email(empfaenger=[], betreff="", nachricht="", anhang=[]):
    # Email content
    sender = smtp_user  # Absender
    message = nachricht  # Nachricht
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender
    to_field = ", ".join(empfaenger)  # Konvertiere die Liste zu einem String für das E-Mail 'To' Feld
    msg['To'] = to_field
    msg['Subject'] = betreff
    for file_path in anhang:
        with open(file_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{basename(file_path)}"'
            msg.attach(part)

    msg.attach(MIMEText(message, 'plain'))
    # Send the email
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()  # TLS Verschlüsselung
    server.login(smtp_user, smtp_password)
    server.sendmail(sender, empfaenger, msg.as_string())
    server.quit()  # Verbindung beenden


for betreff, receiver_files_tuple in mails_dict.items():
    empfaenger = receiver_files_tuple[0]
    anhang = receiver_files_tuple[1]
    send_email(empfaenger=empfaenger, betreff=betreff, anhang=anhang)
