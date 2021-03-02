import time
import urllib.request
import emailer as em

addr = 'https://www.stcharleshealthcare.org/covidvaccine'

def get_context( ):
    # Open webpage and retreive source
    with urllib.request.urlopen( addr ) as response:
        html = response.read()
        lines = html.splitlines()
    # Scan source for header line
    lc = 0
    for line in lines:
        if "field__item".encode() in line:
            hdr = lc
            break
        lc+=1
    return lines[hdr:hdr+30]

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
            sender.sendmail(recipient3_email_addr, emailSubject, emailContent)
            
            context = scan
            print( 'Emails sent at ' + time.asctime() )
        time.sleep(60)
finally:
    # Inform recipient 1 about program exit
    emailSubject = "vacc_scan stopped!"
    emailContent = time.asctime()
    sender.sendmail(recipient1_email_addr, emailSubject, emailContent)
    print('Program quit email sent at ' + time.asctime() )