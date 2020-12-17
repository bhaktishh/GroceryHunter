# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

def send_msg_to_requester(phone_number, requester_name, volunteer_name):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = 'ACc73e024efbe473a39cdab0937c11fc43'  #os.environ['TWILIO_ACCOUNT_SID']
    auth_token = 'ea1cae1912e39fb08e198f6030b881d0' #os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body='Hi ' + requester_name + ', ' + volunteer_name + ' has taken your request! They will approach soon!',
             from_='+18135484923',
             to=phone_number
         )


print(message.sid)