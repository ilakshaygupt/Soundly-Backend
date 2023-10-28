import random

from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MyUser
from rest_framework.exceptions import APIException
from rest_framework import status

import requests
import os

def send_otp_via_email(email):
    subject="your subject verification email "
    otp=random.randint(1000,9999)
    message= f"your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    user_obj=MyUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()


api_key=os.getenv("API_KEY")

def send_otp_via_sms(phone_number,otp):
    print(api_key)
    requests.get(f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/")

def generate_otp():
    otp = random.randint(1000,9999)
    return otp


class CustomError(APIException):
    def __init__(self, error, code = status.HTTP_400_BAD_REQUEST):
        self.status_code = code
        self.detail = {'message' : [error]}
