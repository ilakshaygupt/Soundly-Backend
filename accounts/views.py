from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer ,UserLoginSerializer ,UserProfileSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from accounts.emails import send_otp_via_email
from accounts.serializers import VerifyAccountSerializer
from accounts.models import MyUser
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_via_email(user.email)
            token =get_tokens_for_user(user)
            return Response({"token" : token,"msg" : "registation succesful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                token =get_tokens_for_user(user)

                return Response({"token" : token,"msg" : "Login succesful"}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": {"NON FIELD ERRORS":"EMAIL OR PASSWORD IS NOT VALID" }}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = (UserRenderer,)
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
from rest_framework_simplejwt.tokens import RefreshToken
class VerifyOtpView(APIView):
    def post(self, request, format=None):
        try:
            serializer = VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
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


