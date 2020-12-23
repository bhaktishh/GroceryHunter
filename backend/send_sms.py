# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

def send_msg_to_requester(requester_phone, volunteer_phone, requester_name, volunteer_name):
    # Your Account Sid and Auth Token from twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = ''  #os.environ['TWILIO_ACCOUNT_SID']
    auth_token = '' #os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body='Hi ' + requester_name + ', ' + volunteer_name + ' has taken your request! They will approach soon! Contact them at ' + volunteer_phone,
             from_='+18135484923',
             to=requester_phone
         )
    #print(message.id)


