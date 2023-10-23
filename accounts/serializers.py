from rest_framework import serializers
from accounts.models import MyUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['email', 'name', 'password', 'password1']
        extra_kwargs = {
            'password1': {'write_only': True},

        }
    def validate(self,data):
        password=data.get('password')
        password1=data.get('password1')
        if password != password1:
            raise serializers.ValidationError("Password must match.")
        return data
    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )
        return user


