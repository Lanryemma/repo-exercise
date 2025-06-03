# -*- coding: utf-8 -*-
"""
Sending email notifications using smtplib

@author: Mayank
"""

import MetaTrader5 as mt5
import os
import time
import smtplib
import ssl
from email.mime.text import MIMEText 

"""
def send_email(message, to_email_id="ololadeolayokun@gmail.com", app_password="hsuqgmnylpnnxzwd", email_id="lanryemma@gmail.com"):
    try:
        # Create a MIME message
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
            #s.login("lanryemma@gmail.com", "hsuqgmnylpnnxzwd")  # No spaces!
            #s.sendmail("lanryemma@gmail.com", "ololadeolayokun@gmail.com", "Subject: Test\n\nHello")
            s.login(email_id,app_password)
            s.sendmail(message, email_id, to_email_id)  # Use msg.as_string()
            print("Email sent!")
    except Exception as e:
        print("Email failed:", e)
"""
def send_email(message, email_id="lanryemma@gmail.com", app_password="hsuqgmnylpnnxzwd", to_email_id="Writershub569@gmail.com"):
    try:
        # Create a MIME message
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
            #s.login("lanryemma@gmail.com", "hsuqgmnylpnnxzwd")  # No spaces!
            #s.sendmail("lanryemma@gmail.com", "ololadeolayokun@gmail.com", "Subject: Test\n\nHello")
            s.login(email_id,app_password)
            email_subject="MT5 TradingBot_1 Notification"
            email_body=message
            s.sendmail(email_id,to_email_id, 'Subject: {}\n\n{}'.format(email_subject, email_body))
            print("Email sent!")
    except Exception as e:
        print("Email failed:",e)


def send_email2(message, email_id="lanryemma@gmail.com", app_password="hsuqgmnylpnnxzwd", to_email_id="ololadeolayokun@gmail.com"):
    try:
        # Create a MIME message
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
            #s.login("lanryemma@gmail.com", "hsuqgmnylpnnxzwd")  # No spaces!
            #s.sendmail("lanryemma@gmail.com", "ololadeolayokun@gmail.com", "Subject: Test\n\nHello")
            s.login(email_id,app_password)
            email_subject="MT5 TradingBot_1 Notification"
            email_body=message
            s.sendmail(email_id,to_email_id, 'Subject: {}\n\n{}'.format(email_subject, email_body))
            print("Email sent!")
    except Exception as e:
        print("Email failed:",e)
"""
# display data on the MetaTrader 5 package
print("MetaTrader5 package author: ",mt5.__author__)
print("MetaTrader5 package version: ",mt5.__version__)

#  establish MetaTrader 5 connection to a specified trading account
# if not mt5.initialize(login=25115284, server="MetaQuotes-Demo",password="4zatlbqx"):
#     print("initialize() failed, error code =",mt5.last_error())
#     quit()

#an easier way to establish connection is buy reading the login details from another file
#"os.chdir"--- to change file directory
file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5_Python\\keyfusionmarket.txt"
#file_path = "C:\\Users\\user\Documents\\LANRE\Desktop\\FRONTEND\\Mt5 Python\\key.txt"
key = open(file_path,"r").read().split()
path1 = "C:\\Users\\user\\AppData\\Roaming\\MetaTrader 5\\terminal64.exe"#For the executable path when we run the code

#since we are importing the user id we must convert it to an integer int(key[0])
if not mt5.initialize(path = path1, login= int(key[0]),password=key[1], server=key[2]):
    #print("initialize() failed, error code =",mt5.last_error())
    print("connection not established")
    
else:
    print("connection established")
    send_email("connection established")
"""



"""
def test_email():
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as s:
            s.login("lanryemma@gmail.com", "hsuqgmnylpnnxzwd")  # No spaces!
            s.sendmail("lanryemma@gmail.com", "ololadeolayokun@gmail.com", "Subject: Test\n\nHello")
            print("Email sent!")
    except Exception as e:
        print("Error:", e)

test_email()
time.sleep(2)
"""