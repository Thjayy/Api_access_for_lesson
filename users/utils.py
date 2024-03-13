import re
from rest_framework.validators import ValidationError
import requests
import threading

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_regex = r'^\+998\d{9}$'

def check_email_or_phone(user_input):
    if re.match(email_regex, user_input) is not None:
        return 'access with email'
    elif re.match(phone_regex, user_input) is not None:
        return 'access with phone number'
    else:
        data = {
            'status': False,
            'message': "Enter an existing email or phone number"
        }
        raise ValidationError(data)
    

class SmsThread(threading.Thread):
    def __init__(self, sms):
        self.sms = sms
        super(SmsThread, self).__init__()

    def run(self):
        send_message(self.sms)
        
def send_message(message_text):
    url = f'https://api.telegram.org/bot6523801257:AAEzDTJ4RlWL_m-IpJLBCSfhcgZkh-Tk9_M/sendMessage'
    params = {
        'chat_id':"765001726",
        'text':message_text,
    }
    response = requests.post(url, data=params)
    return response.json()

def send_sms(sms_text):
    sms_thread = SmsThread(sms_text)
    sms_thread.start()
    sms_thread.join()