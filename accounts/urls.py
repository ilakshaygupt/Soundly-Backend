
from django.contrib import admin
from django.urls import path 
from django.urls.conf import include
from accounts.views import UserRegistrationView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="register"),
    
]
