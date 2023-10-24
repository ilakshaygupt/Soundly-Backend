from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.emails import send_otp_via_email
from accounts.serializers import VerifyAccountSerializer
from accounts.models import MyUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from twilio.rest import Client
from django.conf import settings
import random


def generate_otp():
    # Generate a random 4-digit OTP
    otp = ''.join(random.choice('0123456789') for _ in range(4))
    return otp


def send_otp_via_sms(phone_number, otp):
    phone_number = f'+91{phone_number}'
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        # print(serializer)
        phone_number = ""
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
            phone_number = serializer.initial_data['email']
            serializer.initial_data['email'] = serializer.initial_data['email'] + \
                "@phonenumber.com"
            print(phone_number, serializer.initial_data['email'])
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = MyUser.objects.filter(email=email).first()
            if user:
                return Response({"errors": {"NON FIELD ERRORS": "User with this email already exists"}},
                                status=status.HTTP_400_BAD_REQUEST)
            user = serializer.create(serializer.validated_data)
            if phone_number != "":
                otp = generate_otp()
                send_otp_via_sms(phone_number, otp)
                user.otp = otp
                user.save()
            else:
                send_otp_via_email(user.email)
            return Response({"msg": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
            phone_number = serializer.initial_data['email']
            serializer.initial_data['email'] = serializer.initial_data['email'] + \
                "@phonenumber.com"
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = MyUser.objects.filter(email=email).first()
            if user is not None:
                if phone_number != "":
                    otp = generate_otp()
                    send_otp_via_sms(phone_number, otp)
                    user.otp = otp
                    user.save()
                else:
                    send_otp_via_email(user.email)
                return Response({"msg": "Login successful, OTP sent"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"NON FIELD ERRORS": "User with this email does not exist"}},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = (UserRenderer,)
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    def post(self, request, format=None):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
                email = serializer.initial_data['email']
                otp = serializer.initial_data['otp']
                user = MyUser.objects.filter(email=email)
                if not user.exists():
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                print(user[0].otp, "sendotp")
                if not user[0].otp == otp:
                    return Response({"error": "OTP is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({
                    "msg": "Account verified",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=status.HTTP_200_OK)
            elif serializer.is_valid():
                email = serializer.validated_data.get('email')
                otp = serializer.validated_data.get('otp')
                user = MyUser.objects.filter(email=email)
                if not user.exists():
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                user = user[0]
                if not user.otp == otp:
                    return Response({"error": "OTP is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                return Response({
                    "msg": "Account verified",
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
