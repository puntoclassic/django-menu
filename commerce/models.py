from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from django.utils.text import slugify

from profilo.models import User

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
    name = models.CharField(max_length=255, blank=False, null=False)
    default_category = models.ForeignKey(Category, verbose_name="Categoria di default",
                                         on_delete=models.SET_NULL, blank=True, null=True, name='default_category', related_name='foods')
    active = models.BooleanField(
        verbose_name='Attivo (Si/No)', blank=True, default=True, null=False)
    ingredients = models.TextField(
        verbose_name='Ingredienti', blank=False, null=False)
    price = models.DecimalField(
        verbose_name='Prezzo', max_digits=4, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "cibo"
        verbose_name_plural = "cibi"

class OrderStatus(models.Model):
    description = models.CharField(verbose_name='Descrizione stato',max_length=255,blank=False,null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "stato ordine"
        verbose_name_plural = "stati ordine"

class Order(models.Model):
    customer = models.ForeignKey(User,related_name='orders',name='Cliente',blank=False,null=True,on_delete=models.SET_NULL)
    subTotal = models.DecimalField(verbose_name='Totale', max_digits=4, decimal_places=2,blank=False,null=False)
    shippingCosts  = models.DecimalField(verbose_name='Costi di consegna', max_digits=4, decimal_places=2,blank=True,null=False)
    shippingAddress = models.TextField(verbose_name='Indirizzo di consegna',blank=True,null=True)
    shippingDeliveryTime = models.TextField(verbose_name='Orario di consegna',blank=True,null=True)
    shippingRequired = models.BooleanField(verbose_name='Consegna a domicilio',default=False)
    orderStatus = models.ForeignKey(OrderStatus,blank=False,null=True,on_delete=models.SET_NULL,verbose_name='Stato ordine')
    note = models.TextField(blank=True,null=True,verbose_name='Note ordine')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = "ordine"
        verbose_name_plural = "ordini"