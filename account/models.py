from django.contrib.auth.models import AbstractUser
from django.db import models

from .model_fields import LowercaseEmailField
from .manager import UserManager


class Teammate(models.Model):
    nickname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Team(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    email = LowercaseEmailField(unique=True)
    is_active = models.BooleanField(default=False)
    bio = models.CharField(max_length=800, null=True)
    profile_photo = models.ImageField(upload_to='media/images/', null=True, default='photo.jpg')
    teammates = models.ForeignKey(Teammate, null=True, blank=True, on_delete=models.CASCADE)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_perms(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

