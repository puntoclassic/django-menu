from django.db import models
from solo.models import SingletonModel

# Create your models here.
class GeneraliModel(SingletonModel):
    site_name = models.CharField(max_length=255, default='Site Name',verbose_name='Nome del Sito')
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Generali"

    class Meta:
        verbose_name = "generali"
