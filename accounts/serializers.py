import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import MyUser

from .models import MyUser


class UserRegistrationEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, error_messages={'blank': 'Email cannot be blank',
                                                                   'invalid': 'Email format is not valid',
                                                                   'unique': 'User with this Email already exists'})
    username = serializers.CharField(error_messages={'blank': 'Username cant be blank',
                                                     'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['username', 'email']

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        user = MyUser.objects.create_user(
            email=email,
            username=username,
            phone_number=None,
        )
        return user




class UserRegistrationPhoneSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=10, min_length=10, error_messages={
                                         'blank': 'Phone number cannot be blank',
                                         'min_length': 'Phone number should be 10 digits',
                                         'max_length': 'Phone number should be 10 digits'})
    username = serializers.CharField(error_messages={
                                     'blank': 'Username cant be blank',
                                     'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['username', 'phone_number']

    def create_phone_user(self, validated_data):
        username = validated_data.get('username')
        phone_number = validated_data.get('phone_number')
        user = MyUser.objects.create_user(
            email=None,
            username=username,
            phone_number=phone_number,
        )
        return user

class ForgotEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, error_messages={'blank': 'Email cannot be blank',
                                                                   'invalid': 'Email format is not valid',
                                                                   'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['email']

class ForgotPhoneSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=10)

    class Meta:
        model = MyUser
        fields = ['phone_number']

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, error_messages={'blank': 'Username cant be blank',
                                                                     'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['username']

class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, error_messages={'blank': 'Username cant be blank',
                                                                     'unique': 'User with this Email already exists'})
    otp = serializers.CharField(max_length=4, error_messages={
                                'blank': 'otp cannot be blank',
                                'min_length': 'otp should be 4 digits',
                                'max_length': 'otp should be 4 digits'
                                })

class VerifyForgotEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, error_messages={'blank': 'Email cannot be blank',
                                                                   'invalid': 'Email format is not valid',
                                                                   'unique': 'User with this Email already exists'})
    otp = serializers.CharField(max_length=4, error_messages={
                                'blank': 'otp cannot be blank',
                                'min_length': 'otp should be 4 digits',
                                'max_length': 'otp should be 4 digits'
                                })

class VerifyForgotPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=10, max_length=10, error_messages={
                                         'blank': 'Phone number cannot be blank',
                                         'min_length': 'Phone number should be 10 digits',
                                         'max_length': 'Phone number should be 10 digits'})
    otp = serializers.CharField(max_length=4,min_length=4, error_messages={
                                'blank': 'otp cannot be blank',
                                'min_length': 'otp should be 4 digits',
                                'max_length': 'otp should be 4 digits'
                                })
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['username','email','phone_number','profile_pic_url','is_artist','is_valid']

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['profile_pic_url','is_artist']
