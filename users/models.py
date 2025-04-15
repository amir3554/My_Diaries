from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)


    def __str__(self):
        return self.first_name + ' ' + self.last_name
