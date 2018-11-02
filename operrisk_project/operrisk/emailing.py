#this file contains send_email() function than connects to exchange server and sends an e-mail
#from django.conf import settings
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, Configuration
import os


def read_key(fn):#function is used to read *.key files
    key = None   
    if os.path.isdir('keys'):
        key_file = 'keys/'+fn+'.key'
    else:
        key_file = '../keys/'+fn+'.key'
    
    try:
        with open(key_file,'r') as f:
            key = f.readline().strip()
    except:
        raise IOError(key_file+' file not found')
    return key


def send_email(msg_subject,msg_body,msg_recipient_email):
    EXCHANGE_USERNAME = read_key('EXCHANGE_USERNAME')
    EXCHANGE_PASSWORD = read_key('EXCHANGE_PASSWORD')
    PRIMARY_SMTP_ADDRESS = read_key('PRIMARY_SMTP_ADDRESS')
    EXCHANGE_SERVER = read_key('EXCHANGE_SERVER')

    credentials = Credentials(username=EXCHANGE_USERNAME, password=EXCHANGE_PASSWORD)
    config = Configuration(server=EXCHANGE_SERVER, credentials=credentials)
    my_account = Account(primary_smtp_address=PRIMARY_SMTP_ADDRESS, config=config, autodiscover=False, access_type=DELEGATE)


    m = Message(
        account=my_account,
        subject=msg_subject,
        body=msg_body,
        to_recipients=[
            Mailbox(email_address=msg_recipient_email),          
        ]
    )
    m.send()

if __name__ == '__main__':
    print("sending test email...")
    msg_subject = 'База опер.рисков - создан новый инцидент'
    msg_body = 'В базе опер.рисков был создан новый инцидент'
    msg_recipient_email = 'a.mokhnatkin@a-i.kz'
    send_email(msg_subject,msg_body,msg_recipient_email)
    print("email sent")