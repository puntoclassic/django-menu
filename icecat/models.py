from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from commerce.models import Category, Manufacturer

# Create your models here.
class IcecatCategory(MPTTModel):
    name = models.CharField(max_length=255,blank=False,null=False)
    icecat_id = models.IntegerField(blank=False,null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name='Categoria padre')
    shop_category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True,related_name='categorie_icecat')

    def __str__(self) -> str:
        return f"{self.name} ({self.icecat_id})"

    class Meta:
        verbose_name_plural = "categorie Icecat"
        verbose_name = "categoria Icecat"

class IcecatManufacturer(MPTTModel):
    name = models.CharField(max_length=255,blank=False,null=False)
    icecat_id = models.IntegerField(blank=False,null=False)   
    shop_manufacturer= models.ForeignKey(Manufacturer,on_delete=models.SET_NULL,blank=True,null=True,related_name='marche_icecat')

    def __str__(self) -> str:
        return f"{self.name} ({self.icecat_id})"

    class Meta:
        verbose_name_plural = "marche Icecat"
        verbose_name = "marca Icecat"