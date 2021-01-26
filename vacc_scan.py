import time
import urllib.request
import smtplib

## User Input

addr = 'https://www.co.monterey.ca.us/government/departments-a-h/health/diseases/2019-novel-coronavirus-covid-19/vaccination-registration'
sender_gmail_username = 'SENDER@gmail.com'
sender_gmail_password = 'SENDER_PASSWORD'
recipient1_email_addr = 'RECIPIENT1@gmail.com'
recipient2_email_addr = 'RECIPIENT2@gmail.com'

## End User Input

#Email Variables
SMTP_SERVER    = 'smtp.gmail.com'      #Email Server (don't change!)
SMTP_PORT      = 587                   #Server Port (don't change!)
GMAIL_USERNAME = sender_gmail_username
GMAIL_PASSWORD = sender_gmail_password

class Emailer:
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
        
sender = Emailer()

def get_context( ):
    # Open webpage and retreive source
    with urllib.request.urlopen( addr ) as response:
        html = response.read()
        lines = html.splitlines()
    # Scan source for header lines
    lc = 0
    for line in lines:
        begin = line.find( 'Register for a Vaccination Appointment'.encode() )
        end = line.find( 'Directions to Locations'.encode() )
        if begin > -1:
            hl1 = lc
        elif end > -1:
            hl2 = lc
            break
        lc += 1
    # Return content between header lines
    return lines[hl1+1:hl2]

context = get_context( )

try:
    while True:
        # Get new scan of webpage vaccine registration content
        scan = get_context( )
        print( 'Scanned at ' + time.asctime() )
        if scan != context:
            emailSubject = "COVID Vaccine Registration Changes"
            emailContent = "NEW CHANGES " + str(scan)
            sender.sendmail(recipient1_email_addr, emailSubject, emailContent)
            sender.sendmail(recipient2_email_addr, emailSubject, emailContent)
            
            context = scan
            print( 'Emails sent at ' + time.asctime() )
        time.sleep(60)
finally:
    # Inform recipient 1 about program exit
    emailSubject = "vacc_scan stopped!"
    emailContent = time.asctime()
    sender.sendmail(recipient1_email_addr, emailSubject, emailContent)
    print('Program quit email sent at ' + time.asctime() )
