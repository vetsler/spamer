
#!/usr/bin/env python
# encoding: utf-8
"""
python_3_email_with_attachment.py
Created by Robert Dempsey on 12/6/14.
Copyright (c) 2014 Robert Dempsey. Use at your own peril.
This script works with Python 3.x
NOTE: replace values in ALL CAPS with your own values
"""
import sys
import glob, os
import time

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


COMMASPACE = ', '

def send_email(sender, gmail_password, recipients,  subject, text, attachments, prefix):  
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = subject
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    # outer.preamble = preamble

    # List of attachments
    outer.attach(MIMEText(text))

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(prefix+file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise


sender = 'evgps2@gmail.com'
gmail_password = ''
recipient = ['evgps@ya.ru']#'vetsler@gmail.com']
subject = u'Тест спама'
text = u'Тест спама по закидыванию порно в папку'
# files = ['attach.jpg']
while(1):
    for root, dirs, files in os.walk('to_be_sent/'):
        if files  == []:
            time.sleep(5)
        else:
            send_email(sender, gmail_password, recipient,  subject, text, files, 'to_be_sent/')
            for file in files:
                os.rename('to_be_sent/'+file, 'sent/'+file)

