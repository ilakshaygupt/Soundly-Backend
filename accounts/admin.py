from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser

class UserModelAdmin(BaseUserAdmin):
    list_display = ["id", "email", "name", "is_admin"]
    list_filter = ["is_admin"]
    # fieldsets = [
    #     (None, {"fields": ["email", "password", "password1"]}),
    #     ("Personal info", {"fields": ["name"]}),
    #     ("Permissions", {"fields": ["is_admin"]}),
    # ]
    # add_fieldsets = [
    #     (
    #         None,
    #         {
    #             "classes": ["wide"],
    #             "fields": ["email", "name", "password", "password1", "is_admin"],
    #         },
    #     ),
    # ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

admin.site.register(MyUser)
