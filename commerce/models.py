from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
import requests
from django.contrib.auth.models import AbstractUser
from shop.settings import BASE_DIR

# Create your models here.


class Category(MPTTModel):
    name = models.CharField(max_length=100, blank=False,
                            null=False, verbose_name='Nome')
    active = models.BooleanField(verbose_name='Attiva (Si,No)', default=True)
    level = models.IntegerField(
        verbose_name='Livello', editable=False, default=1, null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children', verbose_name='Categoria padre')
    image = models.ImageField(upload_to='public/assets/images/c',
                              blank=True, null=True, verbose_name='Immagine categoria')
    slug = models.SlugField(verbose_name='Slug', editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        anchestors = self.get_ancestors(include_self=True)
        slug_list = []
        for anc in anchestors:
            slug_list.append(slugify(anc.name))
        self.slug = "/".join(slug_list)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorie"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, blank=False,
                            null=False, verbose_name='Nome')
    active = models.BooleanField(verbose_name='Attiva (Si,No)', default=True)
    image = models.ImageField(
        upload_to='public/assets/images/m', blank=True, null=True, verbose_name='Logo')
    imageUrl = models.URLField(
        blank=True, null=True, verbose_name='URL Logo scaricabile')

    def download_logo(self):
        if self.imageUrl != "" or self.imageUrl is not None:
            content = requests.get(self.imageUrl).content
            if content:
                extension = self.imageUrl.split("/")[-1].split(".")[1]
                image_file_path = f"public/assets/images/m/{self.id}.{extension}"
                image_file = open(image_file_path, "wb")
                image_file.write(content)
                image_file.close()
                self.image = image_file_path
                self.save()
            return True
        return False

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marche"

    def __str__(self):
        return self.name


class CommerceUser(AbstractUser):
    tipologia = models.CharField(choices=[
        ('PRIVATO', 'Privato'),
        ('AZIENDA', 'Azienda'),
        ('PUBBLICA_AMMINISTRAZIONE', 'Pubblica Amministrazione'),
        ('ASSOCIAZIONE', 'Associazione')
    ], blank=False, null=False, default='Privato', max_length=200)
