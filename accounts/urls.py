
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from accounts.views import (UserLoginView, UserProfileView,
                            UserRegistrationPhoneView,UserRegistrationEmailView, VerifyOtpView)

urlpatterns = [
    path('register/email', UserRegistrationEmailView.as_view(), name="register"),
    path('register/phone', UserRegistrationPhoneView.as_view(), name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    path('verify/', VerifyOtpView.as_view(), name='verify')
]
