from hashlib import blake2b
from tokenize import blank_re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify

# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=100,blank=False,null=False,verbose_name='Nome')
    active = models.BooleanField(verbose_name='Attiva (Si,No)',default=True)
    level = models.IntegerField(verbose_name='Livello',editable=False,default=1,null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name='Categoria padre')
    image = models.ImageField(upload_to='public/assets/images/c',blank=True,null=True,verbose_name='Immagine categoria')
    slug = models.SlugField(verbose_name='Slug',editable=False)

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
    name = models.CharField(max_length=100,blank=False,null=False,verbose_name='Nome')
    active = models.BooleanField(verbose_name='Attiva (Si,No)',default=True)    
    image = models.ImageField(upload_to='public/assets/images/m',blank=True,null=True,verbose_name='Logo')
    imageUrl = models.URLField(blank=True,null=True, verbose_name='URL Logo scaricabile')

    def download_logo(self):
        if self.imageUrl != "" or self.imageUrl is not None:
            pass
        pass

    class Meta:
        verbose_name = "marca"
        verbose_name_plural = "marche"

    def __str__(self):
        return self.name


