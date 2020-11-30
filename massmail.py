import argparse
import pandas
import ssl
import smtplib
import time
import email
import email.mime.multipart
import email.mime.text

from getpass import getpass
from os import path

from constants import SUBJECT, BODY

data = None                                  # email and recepient emails
smtp_server = "smtp.gmail.com"               # smtp server name
port = 587                                   # for starttls
sender_email = None                          # your email
password = None                              # your password
context = ssl.create_default_context()       # create a secure SSL context
server = None                                # mail server

class Email:
    '''class representing an email'''    

    def __init__(self, recepient, subject, body):
        '''Email constructor'''
        self.recepient = recepient
        self.subject = subject
        self.body = body

    def __str__(self):
        '''returns a string representation of the email'''
        return "----------------------\n" + \
            f"Recipient: {self.recepient} \n\n" + \
            f"Subject: {self.subject} \n\n" + \
            f"Body: {self.body}\n" + \
            "----------------------\n\n"

    def send(self):
        '''sends email using a mail object'''
        global sender_email, server
        msg = email.mime.multipart.MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = self.recepient
        recipients = [self.recepient]
        msg['Subject'] = self.subject
        msg.attach(email.mime.text.MIMEText(self.body, 'plain'))
        server.sendmail(sender_email, self.recepient, msg.as_string())

    def send_test(self):
        '''tests sends email using a mail object'''
        global sender_email, server
        msg = email.mime.multipart.MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sender_email
        recipients = [sender_email]
        msg['Subject'] = self.subject
        msg.attach(email.mime.text.MIMEText(self.body, 'plain'))
        server.sendmail(sender_email, sender_email, msg.as_string())

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()

def parse_data():
    '''parses data from data.csv'''
    global data
    if not path.isfile("data.csv"):
        raise Exception("data.csv does not exist")
    df = pandas.read_csv("data.csv")
    if len(df) <= 1:
        raise Exception("data.csv has at most 1 row, send a single email manually please")
    if "email" not in list(df.columns):
        raise Exception("data.csv does not contain email field")
    data = df

def generate_samples():
    '''creates a 3 sample emails to display'''
    emails = []
    records = data.to_dict('records')
    for i in range(min(3,len(data))):
        r = records[i]
        e = Email(r["email"], SUBJECT.format(**r), BODY.format(**r))
        emails.append(e)
    return emails

def run_sample():
    emails = generate_samples()
    print("Sample emails:")
    for e in emails:
        print(e)
    print("**************************************************")

def run_test():
    '''sends sample emails back to self'''
    print("Sending sample emails to sender email")
    emails = generate_samples()
    for e in emails:
        e.send_test()
    print("Sucess!")
    print("**************************************************")

def init_email():
    '''initializes SMTP gmail server'''
    global sender_email, password, server, port, context
    print("Please enter the appropriate information to login to email.")
    time.sleep(0.5)
    sender_email = input("Please enter your gmail. ")
    while(type(sender_email) != str 
        or len(sender_email) < 10  
        or sender_email[-10:] != "@gmail.com"):
        sender_email = input("Please enter a valid gmail. ")
    password = getpass()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo()
        server.login(sender_email, password)
        # TODO: Send email here
        # print("hi")
    except Exception as e:
        raise Exception("Invalid gmail and password combination or insecure apps disallowed\n \
        visit https://myaccount.google.com/u/3/lesssecureapps to allow less secure apps")
    print("Successfully connected to mail server")
    print("**************************************************")
    
def run_mass_emailer():
    '''run mass emailer including checks'''
    print("Running mass emailer and checks")
    global server
    if server == None:
        raise Exception("email server has not been initialized")
    run_sample()
    confirmation = input("Is this sample correct? [y/n] ")
    if len(str(confirmation)) < 1 or str(confirmation)[0].lower() != "y":
        print("Confirmation on samples failed, please make edits and try again. ")
        return
    records = data.to_dict('records')
    for i in range(len(data)):
        r = records[i]
        e = Email(r['email'], SUBJECT.format(**r), BODY.format(**r))
        e.send()
        print(f"Email successfully sent to {r['email']}, sent {i+1}/{len(data)}")
        time.sleep(0.1)
    
    print(f"Successfully sent {len(data)} emails!")
    print("**************************************************")
    return 

def get_options():
    '''function for getting command line arguments'''
    aparser = argparse.ArgumentParser(description="email parameters")
    aparser.add_argument("-sample", action="store_true", help="view sample emails")
    aparser.add_argument("-test", action="store_true", help="test email")
    opts = vars( aparser.parse_args() )
    return opts

def main():
    '''entry point to program'''
    opts = get_options()
    parse_data()
    if opts["sample"]:
        run_sample()
        return
    else:
        init_email()
        if opts["test"]:
            run_test()
        else:
            run_mass_emailer()
        server.quit()


if __name__ == "__main__":
    main()