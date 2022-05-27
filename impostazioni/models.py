from django.db import models
from solo.models import SingletonModel

# Create your models here.
class GeneraliModel(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name',verbose_name='Nome del Sito')
    maintenance_mode = models.BooleanField(default=False)
    site_description = models.TextField(verbose_name='Descrizione del sito (verrà usata nel tag Description sulla home',blank=True,null=False,default='')
    site_keywords = models.TextField(verbose_name='Parole chiave del sito (verranno usate nel tag Keywords sulla home',blank=True,null=False,default='')


    def __str__(self):
        return "Generali"

    class Meta:
        verbose_name = "generali"
