import re

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import MyUser

from .models import MyUser
from .utils import send_otp_via_email , send_otp_via_sms

class UserRegistrationEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, error_messages={'blank': 'Email cannot be blank',
                                                                   'invalid': 'Email format is not valid',
                                                                   'unique': 'User with this Email already exists'})
    username = serializers.CharField(error_messages={'blank': 'Username cant be blank',
                                                     'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['username', 'email']
    def validate_email(self, value):
        value = value.lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Email format is not valid")
        if MyUser.objects.filter(email=value).exists() and MyUser.objects.filter(email=value).first().is_valid:
            raise ValidationError("User with this Email already exists")
        if MyUser.objects.filter(email=value).exists() and not MyUser.objects.filter(email=value).first().is_valid:
            MyUser.objects.filter(email=value).first().delete()
        return value
    def validate_username(self, value):
        value = value.lower()
        if MyUser.objects.filter(username=value).exists() and MyUser.objects.filter(username=value).first().is_valid:
            raise ValidationError("User with this Username already exists")
        if MyUser.objects.filter(username=value).exists() and not MyUser.objects.filter(username=value).first().is_valid:
            MyUser.objects.filter(username=value).first().delete()
        return value
    def create(self, validated_data):
        username = validated_data.get('username').lower()
        email = validated_data.get('email').lower()
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
    def validate_username(self, value):
        value = value.lower()
        if MyUser.objects.filter(username=value).exists() and MyUser.objects.filter(username=value).first().is_valid:
            raise ValidationError("User with this Username already exists")
        if MyUser.objects.filter(username=value).exists() and not MyUser.objects.filter(username=value).first().is_valid:
            MyUser.objects.filter(username=value).first().delete()
        return value
    def validate_phone_number(self, value):
        value = value.lower()
        if not re.match(r"^[0-9]*$", value):
            raise ValidationError("Phone number should be digits")
        if len(value) != 10:
            raise ValidationError("Phone number should be 10 digits")
        if MyUser.objects.filter(phone_number=value).exists() and MyUser.objects.filter(phone_number=value).first().is_valid:
            raise ValidationError("User with this Phone number already exists")
        if MyUser.objects.filter(phone_number=value).exists() and not MyUser.objects.filter(phone_number=value).first().is_valid:
            MyUser.objects.filter(phone_number=value).first().delete()
        return value
    

    def create(self, validated_data):
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
    def validate_email(self, value):
        value = value.lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValidationError("Email format is not valid")
        if not MyUser.objects.filter(email=value).exists() and MyUser.objects.filter(email=value).first().is_valid:
            raise ValidationError("User with this Email does not exists")
        if not MyUser.objects.filter(email=value).exists() and not MyUser.objects.filter(email=value).first().is_valid:
            raise ValidationError("User with this Email is not Verified")
        return value
    def send_email(self, validated_data):
        email = validated_data.get('email').lower()
        user = MyUser.objects.filter(email=email).first()
        send_otp_via_email(user.email)
        return user.username

class ForgotPhoneSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=10)

    class Meta:
        model = MyUser
        fields = ['phone_number']
    def validate_phone_number(self, value):
        value = value.lower()
        if not re.match(r"^[0-9]*$", value):
            raise ValidationError("Phone number should be digits")
        if len(value) != 10:
            raise ValidationError("Phone number should be 10 digits")
        if not MyUser.objects.filter(phone_number=value).exists() and MyUser.objects.filter(phone_number=value).first().is_valid:
            raise ValidationError("User with this Phone number does not exists")
        if not MyUser.objects.filter(phone_number=value).exists() and not MyUser.objects.filter(phone_number=value).first().is_valid:
            raise ValidationError("User with this Phone number is not Verified")
        return value
    def send_phone(self, validated_data):
        phone_number = validated_data.get('phone_number').lower()
        user = MyUser.objects.filter(phone_number=phone_number).first()
        send_otp_via_sms(user.phone_number,)
        return user.username


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, error_messages={'blank': 'Username cant be blank',
                                                                     'unique': 'User with this Email already exists'})

    class Meta:
        model = MyUser
        fields = ['username']

    def validate_username(self, value):
        value = value.lower()
        if not MyUser.objects.filter(username=value).exists():
            raise ValidationError("User with this Username does not exist")
        if not MyUser.objects.filter(username=value, is_valid=True).exists():
            raise ValidationError("User with this Username is not verified")
        
        return value
    
    def send_otp(self, validated_data):
        user = MyUser.objects.filter(username=validated_data.get('username')).first()
        if user.phone_number:
            send_otp_via_sms(user.phone_number)
        else:
            send_otp_via_email(user.email)
        return user.username


class VerifyAccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, error_messages={'blank': 'Username cant be blank',
                                                                     'unique': 'User with this Email already exists'})
    otp = serializers.CharField(max_length=4, error_messages={
                                'blank': 'otp cannot be blank',
                                'min_length': 'otp should be 4 digits',
                                'max_length': 'otp should be 4 digits'
                                })

    def validate_username(self,value):
        value = value.lower()
        if not MyUser.objects.filter(username=value).exists():
            raise ValidationError("User with this Username does not exist")
        if not MyUser.objects.filter(username=value, is_valid=True).exists():
            raise ValidationError("User with this Username is not verified")
        return value
    def validate_otp(self, value):
        value = value.lower()
        if not value:
            raise ValidationError("OTP already used")
        if not re.match(r"^[0-9]*$", value):
            raise ValidationError("otp should be digits")
        if len(value) != 4:
            raise ValidationError("otp should be 4 digits")
        return value
    def validate(self, data):
        username = data.get('username')
        otp = data.get('otp')
        user = MyUser.objects.filter(username=username).first()
        if not user.otp:
            raise ValidationError("OTP already used")
        if not user.otp == otp:
            raise ValidationError("Invalid otp")
        user.is_valid = True
        user.otp = None
        user.save()
        return data
        


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
    otp = serializers.CharField(max_length=4, min_length=4, error_messages={
                                'blank': 'otp cannot be blank',
                                'min_length': 'otp should be 4 digits',
                                'max_length': 'otp should be 4 digits'
                                })


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'phone_number',
                  'profile_pic_url', 'is_uploader', 'is_valid']


class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, error_messages={

    })
    class Meta:
        model = MyUser
        fields = ['profile_pic_url', 'is_uploader']