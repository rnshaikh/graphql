from django.db import models

from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)

from django.contrib.auth.password_validation import validate_password


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        if password:
            validate_password(password)
        UserManager.normalize_email(email)
        user = self.model(email=email, password=password, **kwargs)

        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1)
    password = models.CharField(max_length=256)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
