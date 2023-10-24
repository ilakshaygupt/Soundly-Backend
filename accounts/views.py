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
from accounts.serializers import (UserLoginSerializer, UserProfileSerializer,
                                  UserRegistrationSerializer,
                                  VerifyAccountSerializer)
from accounts.utils import *



class UserRegistrationView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        phone_number = ""
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
            phone_number = serializer.initial_data['email']
            serializer.initial_data['email'] = serializer.initial_data['email'] + \
                "@phonenumber.com"
        elif serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) != 10:
            return Response({"errors": "Invalid Number"}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = MyUser.objects.filter(email=email).first()
            if user:
                return Response({"errors": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.create(serializer.validated_data)
            if phone_number != "":
                otp = generate_otp()
                send_otp_via_sms(phone_number, otp)
                user.otp = otp
                user.save()
            else:
                send_otp_via_email(user.email)
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        phone_number = ""
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
            phone_number = serializer.initial_data['email']
            serializer.initial_data['email'] = serializer.initial_data['email'] + \
                "@phonenumber.com"
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) != 10:
            return Response({"errors": "Invalid Number"}, status=status.HTTP_400_BAD_REQUEST)
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
                return Response({
                    "message": "Login Succesful , OTP sent"
            }, status=status.HTTP_200_OK)
            else:

                return Response({"email": "User with this email or phone number does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
class VerifyOtpView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.initial_data['email'].isdigit() and len(serializer.initial_data['email']) == 10:
            serializer.initial_data['email'] = serializer.initial_data['email'] + "@phonenumber.com"
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            otp = serializer.validated_data.get('otp')
            user = MyUser.objects.filter(email=email)
            if not user.exists():
                return Response({
                        "email": "User does not exist"
                }, status=status.HTTP_400_BAD_REQUEST)
            user = user[0]
            if not user.otp == otp:
                return Response({

                        "otp": ["Invalid otp"]

                }, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({

                    "access_token": access_token,
                    "refresh_token": refresh_token

            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
