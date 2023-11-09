
from django.urls import path

from accounts.views import *

urlpatterns = [
    path('register/email/', UserRegistrationEmailView.as_view(), name="register"),
    path('register/phone/', UserRegistrationPhoneView.as_view(), name="register"),
    path('verify/', VerifyOtpView.as_view(), name='verify'),
    path('login/', UserLoginView.as_view(), name="login"),
    path('forgot-email/', ForgotEmail.as_view(), name='forgot-email'),
    path('forgot-phone_number/', ForgotPhone.as_view(),
         name='forgot-phone_number'),
    path('profile/', UserProfie.as_view(), name='profile'),
    path('profile/update/', UpdateProfile.as_view(), name='profile-update'),
]
