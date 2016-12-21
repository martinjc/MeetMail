import config
import argparse
from meetapi import MeetApi
from mailer import MeetMail

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Using the meetup calendar to generate an email')
    parser.add_argument('-l', '--limit', help='Limited to that month only', required=False, action="store_true")
    parser.add_argument('-d', '--dev', help='Testing purposes', required=False, action="store_true")
    parser.add_argument('-e', '--email', help='Send email straight to all the people!', required=False, action="store_true")
    parser.add_argument('-i','--in_file', help='Input file name',required=False)
    parser.add_argument('-r','--reminder',help='Name of meetup reminder', required=False)
    args = parser.parse_args()

    MA = MeetApi(reminder=args.reminder, limit=args.limit, in_file=args.in_file)
    MSG = config.email_reminder.format(args.reminder) if args.reminder else config.email_welcome.format(MA.months[MA.today.month-1])
    SUB, MEETUPS = MA.gen_meetups()
    MSG += MEETUPS
    MSG += config.email_rem_close if args.reminder else config.email_close
    
    MAILER = MeetMail(SUB, MSG)
    if args.dev:
        print(MSG)
    else:
        MAILER.send(config.uname, config.pwd)

