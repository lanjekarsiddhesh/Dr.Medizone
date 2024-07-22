import os
from dotenv import load_dotenv, dotenv_values
load_dotenv() 

def ApiKey():
    RAZORPAY_API_KEY = os.getenv("RAZORPAY_API_KEY_value")
    RAZORPAY_API_SECRET_KEY = os.getenv("RAZORPAY_API_SECRET_KEY_value")

    return {"RKey":RAZORPAY_API_KEY,"RSecretKey":RAZORPAY_API_SECRET_KEY}