from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email_verified = models.BooleanField(default=False,verbose_name='Email verificata')
    activation_code = models.CharField(max_length=10,null=True,blank=True)
