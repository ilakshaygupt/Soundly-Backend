import random

import requests
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import MyUser
from accounts.renderers import UserRenderer
from accounts.serializers import *
from accounts.utils import *


class UserRegistrationEmailView(APIView):
    renderer_classes=[UserRenderer]

    def post(self, request, format=None):

        serializer = UserRegistrationEmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user = MyUser.objects.filter(username=username).first()
            if user:
                return Response({"errors": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if MyUser.objects.filter(email=email).exists():
                return Response({"errors": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.create(serializer.validated_data)
            send_otp_via_email(user.email)
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationPhoneView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationPhoneSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            phone_number = serializer.validated_data.get('phone_number')
            user = MyUser.objects.filter(username=username).first()
            if user:
                print(user)
                return Response({"errors": "User with this username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            if MyUser.objects.filter(phone_number=phone_number).exists():
                return Response({"errors": "User with this phone number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.create_phone_user({"username":username,"phone_number":phone_number})
            otp = generate_otp()
            send_otp_via_sms(phone_number, otp)
            user.otp = otp
            user.save()
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.core.exceptions import ValidationError
class ForgotEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = ForgotEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = MyUser.objects.filter(email=email).first()
            if not user:
                return Response({"errors": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            otp = generate_otp()

            return Response({"message": "OTP sent to registered Email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPhone(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = ForgotPhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            user = MyUser.objects.filter(phone_number=phone_number).first()
            if not user:
                return Response({"errors": "User with this phone number does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            otp = generate_otp()
            send_otp_via_sms(phone_number, otp)
            user.otp = otp
            user.save()
            return Response({"message": "OTP sent to registered Phone Number"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes=[UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            # Check if a user with the provided username exists
            user = MyUser.objects.filter(username=username).first()
            if user :
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
            else:
                return Response({"message": "User with this username does not exist"}, status=status.HTTP_200_OK)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        user = request.user

        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VerifyOtpView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            username=serializer.validated_data.get('username')
            print(username)
            otp = serializer.validated_data.get('otp')
            user = MyUser.objects.filter(username=username)
            if not user.exists():
                return Response({
                        "message": "User does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            user = user[0]
            if not user.otp == otp:
                return Response({
                        "message": "Invalid otp"
                }, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'message': 'OTP verified successfully',
                'data':{
                    "access_token": access_token,
                    "refresh_token": refresh_token}
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
