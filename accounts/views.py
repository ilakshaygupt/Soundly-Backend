from django.core.exceptions import ValidationError
import random

import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import MyUser
from accounts.renderers import UserRenderer
from accounts.serializers import *
from accounts.utils import *


class UserRegistrationEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):

        serializer = UserRegistrationEmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            try:
                user = MyUser.objects.get(username=username)
                if user and user.is_valid:
                    return Response({"errors": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
                elif user and not user.is_valid:
                    user.delete()
            except:
                user = None
            try:
                user_email = MyUser.objects.get(email=email)
                if user_email and user_email.is_valid:
                    return Response({"errors": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
                elif user_email and not user_email.is_valid:
                    user_email.delete()
            except:
                user_email = None
            newuser = serializer.create(serializer.validated_data)
            send_otp_via_email(newuser.email)
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationPhoneView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationPhoneSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            phone_number = serializer.validated_data.get('phone_number')

            try:
                user = MyUser.objects.get(username=username)
                if user and user.is_valid:
                    return Response({"errors": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
                elif user and not user.is_valid:
                    user.delete()
            except:
                user = None

            try:
                user_phone = MyUser.objects.get(phone_number=phone_number)
                if user_phone and user_phone.is_valid:
                    return Response({"errors": "User with this phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
                elif user_phone and not user_phone.is_valid:
                    user_phone.delete()
            except:
                user_phone = None

            newuser = serializer.create_phone_user(
                {"username": username, "phone_number": phone_number})
            otp = generate_otp()
            send_otp_via_sms(phone_number, otp)
            newuser.otp = otp
            newuser.save()
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#below for valid
class ForgotEmail(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = ForgotEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                # use = MyUser.objects.filter(email=email).first()
                user=MyUser.objects.get(email=email)
                if not user.is_valid:
                    return Response({"errors": "User is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                send_otp_via_email(email)
                user_obj=MyUser.objects.get(email=email)
                user_obj=user_obj.username
                return Response({"message": "OTP sent to registered Email","data": user_obj}, status=status.HTTP_200_OK)
            except:
                return Response({"errors": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#below
class ForgotPhone(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = ForgotPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            try:
                user = MyUser.objects.filter(phone_number=phone_number).first()
                otp = generate_otp()
                send_otp_via_sms(phone_number, otp)
                user.otp = otp
                user.save()
                return Response({"message": "OTP sent to registered Phone Number","data":user.username}, status=status.HTTP_200_OK)
            except:
                return Response({"errors": "User with this phone number does not exist"}, status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            try:
                use = MyUser.objects.filter(username=username).first()
                user=MyUser.objects.get(username=username)

                if user and user.is_valid:
                    if user.phone_number:
                        otp = generate_otp()
                        send_otp_via_sms(user.phone_number, otp)
                        user.otp = otp
                        user.save()
                    else:
                        send_otp_via_email(user.email)
                    phone_number = user.phone_number
                    email = user.email
                    return Response({"message": "Login Successful, OTP sent"}, status=status.HTTP_200_OK)

                elif user and not user.is_valid:
                    return Response({"errors": "User is not verified"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"errors": "User with this username does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            otp = serializer.validated_data.get('otp')
            user = MyUser.objects.filter(username=username)
            if not user.exists():
                return Response({
                        "error": "User does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            user = user[0]
            if not user.otp == otp:
                return Response({
                    "error": "Invalid otp"
                }, status=status.HTTP_400_BAD_REQUEST)
            user.is_valid = True
            user.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'message': 'OTP verified successfully',
                'data': {
                    "access_token": access_token,
                    "refresh_token": refresh_token}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
