import smtplib
# This requires a directory, info/ , and two files within:
#  a blank __init__.py file and a mail_info file which contains
#  the mi.* variables below.
import info.mail_info as mi

sender_gmail_username = mi.sender_gmail_username
sender_gmail_password = mi.sender_gmail_password
recipient1_email_addr = mi.rcpnt1_email_username
recipient2_email_addr = mi.rcpnt2_email_username
recipient3_email_addr = mi.rcpnt3_email_username

#Email Variables
SMTP_SERVER    = 'smtp.gmail.com'      #Email Server (don't change!)
SMTP_PORT      = 587                   #Server Port (don't change!)
GMAIL_USERNAME = sender_gmail_username
GMAIL_PASSWORD = sender_gmail_password

def sendmail(self, recipient, subject, content):
     
    #Create Headers
    headers = ["From: " + GMAIL_USERNAME, "Subject: " + subject, "To: " + recipient,
               "MIME-Version: 1.0", "Content-Type: text/html"]
    headers = "\r\n".join(headers)

    #Connect to Gmail Server
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()

    #Login to Gmail
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

    #Send Email & Exit
    session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
    session.quit