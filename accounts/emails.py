import random

from django.conf import settings
from django.core.mail import send_mail

from .models import MyUser


def send_otp_via_email(email):
    subject="your subject verification meial "
    otp = random.randint(1000,9999)
    message= f"your otp is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    user_obj=MyUser.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
