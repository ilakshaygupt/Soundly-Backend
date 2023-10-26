from rest_framework import serializers

from accounts.models import MyUser


from rest_framework import serializers
from .models import MyUser

class UserRegistrationEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
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


class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['username']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class VerifyAccountSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255)
    otp = serializers.CharField(max_length=4)
