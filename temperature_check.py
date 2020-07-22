#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import json
import time
import os
import smtplib, ssl
from secrets import gmail_passwd, gmail_login

sensors_cmd = "sensors -j"
port = 465

# Safety margin 
SAFETY = 10
# Time to sleep befor shuting down
SLEEPY_TIME_BEFORE_SHUTDOWN = 60 * 5
# Max temperature before you ant it shut down
MAX_TEMPERATURE = 65
# Mail address to send mail
ALERT_MAIL_ADDRESS = 'hello@acortino.me'


def send_mail(subject:str, message : str)->None:
    subject = "[Proxmox] "+subject
    content = 'Subject: {}\n\n{}'.format(subject, message)
    
    context = ssl.create_default_context()
    print(content)
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(gmail_login, gmail_passwd)
        server.sendmail(gmail_login, ALERT_MAIL_ADDRESS, content)


process = subprocess.Popen(sensors_cmd.split(),
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

if not stderr:
    data_sensors = json.loads(stdout)

    ite = 0
    is_max = False
    for data in data_sensors:
        for key, value in data_sensors[data].items():
            if key.startswith('temp') or key.startswith('Core'):
                ite = ite + 1
                temperature = float(value['temp'+str(ite)+'_input'])
                try:
                    max_temperature = float(value['temp'+str(ite)+'_max']) - SAFETY
                except:
                    max_temperature = MAX_TEMPERATURE

                if temperature >= max_temperature:
                    is_max = True            
        if is_max:
            time.sleep(SLEEPY_TIME_BEFORE_SHUTDOWN)
            print("I'm going to shutdown");
            send_mail("Shutdown due to high temperature", "I'm shutting down due to hig temperature \n "+str(data_sensors))
            os.system('systemctl poweroff')
            break

else:
    send_mail("Error getting temperature", str(stderr))
