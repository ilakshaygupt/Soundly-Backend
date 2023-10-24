from rest_framework import serializers
from accounts.models import MyUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'name']
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = MyUser
        fields = ['email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'name',]
        read_only_fields = ['email', 'name',]

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=4)
