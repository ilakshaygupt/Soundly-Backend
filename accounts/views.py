from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):
    def post(self, request,format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg" : "registation succesful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST
        )