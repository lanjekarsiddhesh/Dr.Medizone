from twilio.rest import Client
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv() 

def send_otp():
    twilio_ac = os.getenv("twilio_ac_value")
    ṭwilio_token = os.getenv("twilio_token_value")
    twilio_num = '+16076526286'
    my_num = "+9193590 81178"

    client = Client(twilio_ac,ṭwilio_token)
    message = client.messages.create(
        body="msg",
        from_=twilio_num,
        to=my_num
        )
    
    print(message.sid)