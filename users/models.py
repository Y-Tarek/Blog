from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """ The Base User Model """
    email = models.EmailField(unique=True,error_messages={
            "unique": _("A user with that email already exists."),
        },)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username","first_name","last_name"]

    def __str__(self):
        return self.email

class Profile(models.Model):
    """ The User Profile Model """
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.FileField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return f'{self.user.id}-{self.user.email}'