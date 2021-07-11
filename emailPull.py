import datetime
import smtplib
import time
import imaplib
import email
import traceback 

ORG_EMAIL = "@students.wits.ac.za" 
FROM_EMAIL = "2091295" + ORG_EMAIL 
FROM_PWD = "Hair121314" 
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

def read_email_from_gmail(n):
    ret = []
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[-(n+1)])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']
                    ret.append( email_from) 
                    ret.append(email_subject)
                    ret.append(i)

        return ret

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

latestEmail = 0

emails = read_email_from_gmail(1)
firstIter = False
latestEmail = emails[2]
print(emails)
now = datetime.datetime.now()
oldTime = now.hour*60 + now.minute
i = 0
while True:
    now = datetime.datetime.now()
    currTime = now.hour*60 + now.minute
    if abs(currTime - oldTime) >= 5:
        i += 1
        oldTime = currTime
        emails = read_email_from_gmail(1)
        if(emails[2] != latestEmail):
            latestEmail = emails[2]
            print(emails)
