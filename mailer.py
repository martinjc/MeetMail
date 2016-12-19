import config
import smtplib
from email.mime.text import MIMEText

class MeetMail:

    def __init__(self, body, subject):

        self.msg = MIMEText(body)
        self.subject = subject
        self.to = config.recs
        

    def send(self, uname, pwd):
        """authenticate with SMTP server and send email"""
        smtp_sender = smtplib.SMTP(config.smtp_server, config.smtp_port)
        smtp_sender.ehlo()
        smtp_sender.starttls()
        smtp_sender.login(uname, pwd)
        smtp_sender.sendmail(uname, config.recs + config.bcc, self.msg.as_string())
