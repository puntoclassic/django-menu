
from django.db import models
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from solo.models import SingletonModel
from allauth.account.models import EmailAddress


class User(AbstractUser):
   @property
   def verified(self) -> bool:
    return EmailAddress.objects.filter(email=self.email).first().verified


# Create your models here.
class GeneraliModel(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name',verbose_name='Nome del Sito')  
    shipping_costs = models.DecimalField(verbose_name='Spese di consegna', max_digits=4, decimal_places=2,blank=True,null=False,default=2.00)

    def __str__(self):
        return "Impostazioni generali"

    class Meta:
        verbose_name = "impostazioni generali"
