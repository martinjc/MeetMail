import config
from meetapi import MeetApi
from mailer import MeetMail

MA = MeetApi()
SUB, MSG = MA.gen_meetups()
MAILER = MeetMail(SUB, MSG)
MAILER.send(config.uname, config.pwd)
