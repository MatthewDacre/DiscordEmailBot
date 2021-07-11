import datetime
import smtplib
import time
import imaplib
import email
import traceback
import discord
import os
from dotenv import load_dotenv


#Loading .env file
load_dotenv()


#Using .env file to get target email and password for the email 
FROM_EMAIL =  os.getenv("EMAIL")
FROM_PWD = os.getenv("PASS")
SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

#Setting up discord client
client = discord.Client()


#Pulls n emails from target email
def read_email_from_gmail(n):
    ret = []
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        #Fetchting all emails
        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()   
        first_email_id = int(id_list[-(n+1)])
        latest_email_id = int(id_list[-1])

        #Loops through n eamil IDs, pulling from and subject from each
        for i in range(latest_email_id,first_email_id, -1):
            data = mail.fetch(str(i), '(RFC822)' )

            for response_part in data:
                arr = response_part[0]

                if isinstance(arr, tuple):

                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']
                    email_from = msg['from']

                    #Appends to ret in form [From, Subject, ID]
                    ret.append(email_from) 
                    ret.append(email_subject)
                    ret.append(i)
        
        print("Returing {} emails".format(int(len(ret)/3)))
        return ret

    except Exception as e:
        traceback.print_exc() 
        print(str(e))

@client.event
async def on_ready():
    print("Script Starting")
    #Runs as soon as script loads, send through last 5 emails
    #Done this way so that when the script is run each morning, fecth any possible emails from the previous night.
    #Will be updated to just send through new emails when set up on always on server

    now = datetime.datetime.now()

    #Uses channel ID to find channel to send updates
    channel = client.get_channel(int(os.getenv("CHANNEL")))

    #Fetches 5 most recent emails
    emails = read_email_from_gmail(5)
    print("Fetched Emails: {}".format(emails))
    latestEmail = emails[2]

    #Sends found emails to $channel
    msg = "="*50 + "\n@here\nLast 5 Emails:\n" + "From: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n\nFrom: {}\nSubject: {}\n".format(emails[0], emails[1], emails[3], emails[4], emails[6], emails[7], emails[9], emails[10], emails[12], emails[13])
    await channel.send(msg)

    while True:
        #Loops infinitly, checking for new emails every 5 minutes
        delta = abs((now.now() - now).total_seconds())
        #300s = 5mins
        if delta >= 300:
            print("Checking for new email")
            now = now.now()
            emails = read_email_from_gmail(1)
            if(emails[2] != latestEmail):
                print("Found new email")
                latestEmail = emails[2]
                print("Fetched Email: {}".format(emails))
                msg = "="*50 + "\n@here\nNew Email:\n" + "From: {}\nSubject: {}".format(emails[0], emails[1])
                await channel.send(msg)
            else:
                print("No new email found")


client.run(os.getenv("TOKEN"))