# server-temperature
Check my server temperature and shut it down if it's too high

## General info

Working with Python 3 and lm-sensors

I use it to shutdown my Proxmox when temperature are high. (I only have 1 VM always running with a media server and another one not very important, turned off most of the time)

## Installation

First you have to install and configure lm-sensors
```
$ sudo apt-get install lm-sensors 
```

Then you have to create a new file called secrets.py containing:
```
gmail_passwd = [your gmail password]
gmail_login = [your gmail login]
```

Next, you have to change and customize some parameters in the script:
```
# Safety margin 
SAFETY = 10
# Time to sleep before shutting down
SLEEPY_TIME_BEFORE_SHUTDOWN = 60 * 0.1
# Max temperature to reach to shut it down
MAX_TEMPERATURE = 65
# Mail address to send mail
ALERT_MAIL_ADDRESS = '[receiver address mail]'
```

Then you can put it in a cron to run it every x min:
```
$ crontab -e
```
And add this to run it every 30 min:
```
30 * * * * * python3 <path_to_check_temperature.py>
```
