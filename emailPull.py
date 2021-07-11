import datetime
import smtplib
import time
import imaplib
import email
import traceback
import discord
import os 
 
FROM_EMAIL =  os.getenv("EMAIL")
FROM_PWD = os.getenv("PASS")
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
                    ret.append(email_from) 
                    ret.append(email_subject)
                    ret.append(i)
        return ret

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

client = discord.Client()

@client.event
async def on_ready():
    now = datetime.datetime.now()
    channel = client.get_channel(863720376340447234)
    emails = read_email_from_gmail(5)
    print("Fetched Emails: {}".format(emails))
    latestEmail = emails[2]
    msg = "="*50 + "\n@here\nLast 5 Emails:\n" + "From: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n".format(emails[0], emails[1], emails[3], emails[4], emails[6], emails[7], emails[9], emails[10], emails[12], emails[13])
    await channel.send(msg)

    while True:
        delta = abs((now.now() - now).total_seconds())
        print(delta)
        if delta >= 50:
            print("Entered Loop")
            now = now.now()
            emails = read_email_from_gmail(1)
            print("Last Email ID: {}\nCurr Email ID: {}".format(latestEmail, emails[2]))
            if(emails[2] != latestEmail):
                latestEmail = emails[2]
                print("Fetched Emails: {}".format(emails))
                msg = "="*50 + "\n@here\nNew Email:\n" + "From: {}\nSubject: {}".format(emails[0], emails[1])
                await channel.send(msg)


client.run(os.getenv("TOKEN"))