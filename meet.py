import json
import datetime 
import operator
import argparse
import requests
import pyperclip

months = []
for i in range(1,13):
    months.append(datetime.date(2016, i, 1).strftime('%B'))

def get_meetups(in_file):
    if in_file is None:
        return requests.get("https://api.meetup.com/self/calendar?photo-host=public&page=20&sig_id=24175662&sig=672eb88f247922fd36ad590603c594acc46f630a").json()
    else:
        with open(in_file, 'r') as meetups:
            return json.loads(meetups.read)


def generate_email(meetups, args):
    meetups.sort(key=operator.itemgetter('time'))
    met = []
    today = datetime.datetime.now()
    email_body = """Hello All,
    Welcome to the {0} edition of meetups in and around Cardiff. As usual, we will be heading to the PyDiff meetup as a school outing, but please let us know if there is a meetup you want a group to attend and we will try to organise it! Here is what we have this month and these meetups are only successful because fine people like yourselves keep the Cardiff dev community alive. \n See you there! \n \n """.format(months[today.month-1])
    for meetup in meetups:
        date = datetime.datetime.fromtimestamp(meetup['time'] / 1e3)
        meetup['time'] = date
        name = meetup['name']
        if (name not in met and not args.limit) or (name not in met and args.limit and date.month == today.month):
#and not args.limit) and (args.limit and date.month == today.month):
            # add the name and not the meetup to allow different types of meetup from the same groupto be added
            met.append(name)
            write_meetup(email_body, meetup)

    email_body += """\n\n That pretty much covers it for this month. If you think we are missing anything then please let us know either here or on Twitter (@martinjc and @encima27). \n Thanks! \n Martin and Chris \n \n --- \n Generated by: https://github.com/encima/MeetMail"""
    if args.copy:
        pyperclip.copy(email_body)
        print("Meetup email copied to clipboard")
    if args.output:
        with open(args.output, 'w') as email:
            email.write(email_body)
        print("Meetup email written to: {}".format(args.output))

def write_meetup(email_body, meetup):
    email_body += "\n Name: {} \n".format(meetup['name'])
    email_body += "Meetup: {}\n".format(meetup['group']['name'])
    venue = 'TBC'
    if 'venue' in meetup:
        venue = meetup['venue']['name']
    email_body += "Where: {}\n".format(venue)
    email_body += "When: {}\n".format(meetup['time'])
    email_body += '----- \n'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Using the meetup calendar to generate an email')
    parser.add_argument('-l', '--limit', help='Limited to that month only', required=False, default=False)
    parser.add_argument('-i','--input', help='Input file name',required=False)
    parser.add_argument('-o','--output',help='Output file name', required=False)
    parser.add_argument("-c", "--copy", help="Copy to clipboard", action="store_true")
    args = parser.parse_args()
    meetups = get_meetups(args.input)
    generate_email(meetups, args)
