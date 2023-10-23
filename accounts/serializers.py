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


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = ['email', 'password']

    # def is_valid(self, raise_exception=False):
    #     self._errors = []
    #     return True

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'name','is_active','is_admin']
        read_only_fields = ['email', 'name','is_active','is_admin']