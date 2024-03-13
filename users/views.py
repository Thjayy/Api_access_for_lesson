from django.shortcuts import render
from .serializers import SignUpSerializer
from rest_framework.generics import CreateAPIView
from .models import User, UserCodeVerification, NEW, CODE_VERIFIED, VIA_EMAIL, VIA_PHONE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from datetime import datetime
from .utils import send_sms
# Create your views here.

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class VerifyApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = self.request.user
        if 'code' not in self.request.data:


            data = {
                "status":False,
                "message":"Code field is mandatory"
            }
            raise ValidationError(data)
        
        code = self.request.data['code']
        verify_code = user.confirmation_codes.filter(is_confirmed=False, expire_time__gte=datetime.now(), code=code)

        if not verify_code.exists():
            data = {
                "status":False,
                "message":"Your Code is not available anymore or input is incorrect"
            }
            raise ValidationError(data)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        
        data = {
            "auth_status":user.auth_status,
            "access":user.token()['access'],
            "refresh":user.token()['refresh'],
            "message":"Code is verified"
        }

        return Response(data,status=200)
    
class ResendVerifyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = self.request.user
        self.check_user_code(user)

        if user.auth_type == VIA_EMAIL:
            code = user.create_confirmation_code(VIA_EMAIL)
            send_sms(code)
        
        elif user.auth_type == VIA_PHONE:
            code = user.create_confirmation_code(VIA_PHONE)
            send_sms(code)

        else:
            data = {
                'status': False,
                'message': "The code you sended is incorrect"
            }
            raise ValidationError(data)
        
        data = {
                'status': True,
                'message': "A verification code has been re-sent to you"
            }

    
    def check_user_code(self, user):
        verify_code = user.confirmation_codes.filter(is_confirmed=False, expire_time__gte=datetime.now())
        if verify_code.exists():
            data = {
                'status': False,
                'message': "You already have a verification code, wait.."
            }
            raise ValidationError(data)