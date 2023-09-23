from django.db import models

from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)


class User(AbstractBaseUser):

    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    password = models.CharField(max_length=256)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email
