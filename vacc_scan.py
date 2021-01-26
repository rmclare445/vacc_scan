import time
import urllib.request
import smtplib

addr = 'https://www.co.monterey.ca.us/government/departments-a-h/health/diseases/2019-novel-coronavirus-covid-19/vaccination-registration'

#Email Variables
SMTP_SERVER = 'smtp.gmail.com'    #Email Server (don't change!)
SMTP_PORT = 587                   #Server Port (don't change!)
GMAIL_USERNAME = '[SENDER]@gmail.com'
GMAIL_PASSWORD = '[SENDER_PASSWORD]'

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
    return lines[hl1+1:hl2]

context = get_context( )

try:
    while True:
        scan = get_context( )
        print( 'Scanned at ' + time.asctime() )
        if scan != context:
            emailSubject = "COVID Vaccine Registration Changes"
            emailContent = "NEW CHANGES" + str(scan)
            sender.sendmail('[RECIPIENT_1]@gmail.com', emailSubject, emailContent)
            sender.sendmail('[RECIPIENT_2]@gmail.com', emailSubject, emailContent)
            
            context = scan
            print( 'Emails sent at ' + time.asctime() )
        time.sleep(60)
finally:
    emailSubject = "vacc_scan stopped!"
    emailContent = time.asctime()
    sender.sendmail('[RECIPIENT]@gmail.com', emailSubject, emailContent)
    print('Program quit email sent at ' + time.asctime() )
