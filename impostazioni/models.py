
from tokenize import Single
from django.db import models
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from solo.models import SingletonModel
from allauth.account.models import EmailAddress

from vendite.models import OrderStatus


class User(AbstractUser):
    activation_code = models.CharField(verbose_name='Codice di attivazione',max_length=10,blank=True,null=True)
    @property
    def verified(self) -> bool:
        return EmailAddress.objects.filter(email=self.email).first().verified


# Create your models here.
class ImpostazioniGenerali(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name',verbose_name='Nome del Sito')  

    def __str__(self):
        return "Impostazioni generali"

    class Meta:
        verbose_name = "impostazioni generali"

# Create your models here.
class ImpostazioniSpedizione(SingletonModel):
    shipping_costs = models.DecimalField(verbose_name='Spese di consegna', max_digits=4, decimal_places=2,blank=True,null=False,default=2.00)

    def __str__(self):
        return "Spedizione e consegna"

    class Meta:
        verbose_name = "Spedizione e consegna"

class ImpostazioniOrdini(SingletonModel):
    default_created_state = models.ForeignKey(OrderStatus,verbose_name='Stato per ordine creato',blank=False,null=True,on_delete=models.SET_NULL,related_name='default_created_state_reverse')
    default_paid_state = models.ForeignKey(OrderStatus,verbose_name='Stato per ordine pagato',blank=False,null=True,on_delete=models.SET_NULL,related_name='default_paid_state_reverse')

    def __str__(self):
        return "Ordini"

    class Meta:
        verbose_name = "Ordini"