from rest_framework import serializers

from accounts.models import MyUser
import re


from rest_framework import serializers
from .models import MyUser
from rest_framework.exceptions import ValidationError

class UserRegistrationEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,error_messages={'blank': 'Email cannot be blank',
                                                                  'invalid':'Email format is not valid',
                                                                  'unique':'User with this Email already exists'})
    username = serializers.CharField(error_messages={'blank': 'Username cant be blank',
                                                     'unique':'User with this Email already exists'})
    class Meta:
        model = MyUser
        fields = [ 'username', 'email']



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
    phone_number = serializers.CharField(max_length=10,min_length=10)

    class Meta:
        model = MyUser
        fields = [ 'username', 'phone_number']
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
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email']

class ForgotPhoneSerializer(serializers.ModelSerializer):
    phone_number=serializers.CharField(max_length=10)
    class Meta:
        model = MyUser
        fields = ['phone_number']
class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['username']
    def validate(self, data):
        username = data.get('username')

        # Check if a user with the specified username already exists
        if MyUser.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class VerifyAccountSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255)
