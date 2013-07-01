#!/usr/bin/python
import os, re
import sys
import smtplib
 
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
 
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
 
directory = "html"
 
def sendemail(sender, password, recipient, subject, message):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = recipient
    msg['From'] = sender
 
    files = os.listdir(directory)
    exp = datetime.date.today().isoformat()+".mobi"
    mobisearch = re.compile(exp, re.IGNORECASE)
    files = filter(mobisearch.search, files)
    for filename in files:
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue
 
        mobi = MIMEApplication(open(path, 'rb').read(), _subtype="mobi")
        mobi.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(mobi)
 
    part = MIMEText('text', "plain")
    part.set_payload(message)
    msg.attach(part)
 
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
 
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)
 
    session.sendmail(sender, recipient, msg.as_string())
    session.quit()
