import re
from rest_framework.validators import ValidationError

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