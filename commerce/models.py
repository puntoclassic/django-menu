from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
import requests
from django.contrib.auth.models import AbstractUser
from shop.settings import BASE_DIR

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False,
                            null=False, verbose_name='Nome')
    active = models.BooleanField(verbose_name='Attiva (Si,No)', default=True)    
    image = models.ImageField(upload_to='public/assets/images/c',
                              blank=True, null=True, verbose_name='Immagine categoria')
    slug = models.SlugField(verbose_name='Slug', editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)        
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorie"

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255,blank=False,null=False)
    default_category = models.ForeignKey(Category, verbose_name="Categoria di default", on_delete=models.SET_NULL,blank=True,null=True,name='default_category')    
    active = models.BooleanField(verbose_name='Attivo (Si/No)',blank=True,default=True,null=False)
    ingredients  = models.TextField(verbose_name='Descrizione', blank=True,null=True)

    class Meta:
        verbose_name = "cibo"
        verbose_name_plural = "cibi"

class CommerceUser(AbstractUser):
    tipologia = models.CharField(choices=[
        ('PRIVATO', 'Privato'),
        ('AZIENDA', 'Azienda'),
        ('PUBBLICA_AMMINISTRAZIONE', 'Pubblica Amministrazione'),
        ('ASSOCIAZIONE', 'Associazione')
    ], blank=False, null=False, default='Privato', max_length=200)

