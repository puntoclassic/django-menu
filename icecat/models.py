from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from commerce.models import Category

# Create your models here.
class IcecatCategory(MPTTModel):
    name = models.CharField(max_length=255,blank=False,null=False)
    icecat_id = models.IntegerField(blank=False,null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name='Categoria padre')
    shop_category = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True,null=True,related_name='categorie_icecat')