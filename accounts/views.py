import random

import cloudinary
import requests
from django.core.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import MyUser
from accounts.renderers import UserRenderer
from accounts.serializers import *
from accounts.utils import *
from music.models import Favourite


class UserRegistrationEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):

        serializer = UserRegistrationEmailSerializer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.create(serializer.validated_data)
            send_otp_via_email(newuser.email)
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationPhoneView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserRegistrationPhoneSerializer(data=request.data)
        if serializer.is_valid():
            newuser = serializer.create(serializer.validated_data)
            otp = generate_otp()
            send_otp_via_sms(newuser.phone_number, otp)
            newuser.otp = otp
            newuser.save()
            return Response({"message": "Registration successful, OTP sent"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# below for valid


class ForgotEmail(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = ForgotEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.send_email(serializer.validated_data)
            return Response({"message": "OTP sent to registered Email", "data": user}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# below
class ForgotPhone(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = ForgotPhoneSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.send_phone(serializer.validated_data)
            return Response({"message": "OTP sent to registered Phone number", "data": user}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer,]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username').lower()
            username = serializer.send_otp(validated_data=serializer.validated_data)
            return Response({'message': 'OTP sent to registered Email', "data": username}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    renderer_classes = (UserRenderer,)
    
    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = MyUser.objects.get(username=serializer.validated_data.get('username').lower())
            if not Favourite.objects.filter(user=user).exists():
                Favourite.objects.create(user=user)
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


class UserProfie(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = (UserRenderer,)

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({'message': 'User Data send', "data": serializer.data}, status=status.HTTP_200_OK)

    # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxNjA2OTY5LCJpYXQiOjE2OTkwMTQ5NjksImp0aSI6ImIxZGM3YzAyNWY3MjRiMGJiM2ZmZGVlMDg5Yzk2NjdkIiwidXNlcl9pZCI6ImFua2l0In0.1JekBlVms9r2tS8vsy4EQxzCRq80VhuWKaosjysJiwU  ankit


class UpdateProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (UserRenderer,)

    def patch(self, request):
        try:
            user = MyUser.objects.get(username=request.user)
        except MyUser.DoesNotExist:
            return Response({'message': 'User not found', 'data': ''}, status=status.HTTP_404_NOT_FOUND)
        profile_pic_url = request.user.profile_pic_url
        if 'profile' in request.FILES:
            profile = request.FILES['profile']
            audio_response = cloudinary.uploader.upload(profile, secure=True)
            profile_pic_url = audio_response.get('url')

        serializer = UpdateProfileSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            user.profile_pic_url = profile_pic_url
            user.save()
            return Response({'message': 'User Data Updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
