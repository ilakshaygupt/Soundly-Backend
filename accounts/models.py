
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, User)
from django.db import models
import datetime
from django.utils import timezone

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, phone_number=None):
        """
        Creates and saves a User with the given , username and password.
        """

        user = self.model(
            phone_number=phone_number,
            email=email,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, password=None):
        """
        Creates and saves a superuser with the given  username and password.
        """
        user = self.create_user(
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=10, blank=True, null=True, unique=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    profile_pic_url = models.URLField(
        default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlfrScK05sZxTgh7Bg4p_Anm_ZSxxqGHpCFA&usqp=CAU')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_uploader = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False, null=True, blank=True)
    opt_created_at = models.DateTimeField(auto_now_add=True, null=True)
    # fav_uploader=models.ManyToManyField('self',blank=True,null=True)
    # fav_languages=models.ManyToManyField(Language,blank=True,null=True)
    # fav_playlist=models.ManyToManyField(Playlist,blank=True,null=True)
    # fav_songs=models.ManyToManyField(Song,blank=True,null=True)
    objects = MyUserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    def is_expired(self):
        return self.opt_created_at + datetime.timedelta(seconds=20) <= timezone.now()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
