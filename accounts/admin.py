from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import MyUser

from .models import MyUser, MyUserManager

admin.site.register(MyUser)
