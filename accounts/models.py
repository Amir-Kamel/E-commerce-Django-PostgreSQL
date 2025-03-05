from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoUser

class User(DjangoUser):
    image = models.ImageField(upload_to='images/', default='images/default.jpg')
