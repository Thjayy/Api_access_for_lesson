from rest_framework import serializers
from .models import User, VIA_EMAIL, VIA_PHONE
from .utils import check_email_or_phone
from rest_framework.exceptions import ValidationError

class SignUpSerializer(serializers.ModelSerializer):
    auth_type = serializers.CharField(required=False, read_only=True)
    auth_status = serializers.CharField(required=False, read_only=True)
    
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_or_phonenumber'] = serializers.CharField(required=False)


    class Meta:
        model = User
        fields = ('auth_type', 'auth_status')


    def validate(self, data):
        user_input = data.get('email_or_phone')
        email_or_phone = check_email_or_phone(user_input)
        if email_or_phone == 'phone':
            data = {
                'auth_type':VIA_PHONE,
                'phone_number':user_input
            }
        elif email_or_phone == 'email':
            data = {
                'auth_type':VIA_EMAIL,
                'email_address':user_input
            }
        else:
            data = {
                'status': False,
                'message': "The data you provided is incorrect"
            }
            raise ValidationError(data)
        return data