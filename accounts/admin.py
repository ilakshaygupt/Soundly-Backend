from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser,MyUserManager

from django.contrib import admin
from accounts.models import MyUser

admin.site.register(MyUser)
