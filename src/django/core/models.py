from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	bio = models.TextField(null=True)
	country = models.CharField(max_length=32, null=True)
	picture = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True)
