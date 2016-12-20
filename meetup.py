import config
import argparse
from meetapi import MeetApi
from mailer import MeetMail

parser = argparse.ArgumentParser(description='Using the meetup calendar to generate an email')
parser.add_argument('-l', '--limit', help='Limited to that month only', required=False, action="store_true")
parser.add_argument('-d', '--dev', help='Testing purposes', required=False, action="store_true")
parser.add_argument('-e', '--email', help='Send email straight to all the people!', required=False, action="store_true")
parser.add_argument('-i','--in_file', help='Input file name',required=False)
parser.add_argument('-o','--output',help='Output file name', required=False)
parser.add_argument('-r','--reminder',help='Name of meetup reminder', required=False)
args = parser.parse_args()

MA = MeetApi()
MSG = ""
if args.reminder:
    MSG += config.email_reminder.format(args.reminder)
else:

SUB, MSG = MA.gen_meetups()
MAILER = MeetMail(SUB, MSG)
MAILER.send(config.uname, config.pwd)
