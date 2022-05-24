from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from commerce.models import Category as ShopCategory
from commerce.models import Manufacturer as ShopManufacturer


# Create your models here.


class CategoryExistsOnShopException(Exception):
    pass


class CategoryAlreadyMatchedException(Exception):
    pass


class Category(MPTTModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    icecat_id = models.IntegerField(blank=False, null=False)
    parent_icecat_id = models.IntegerField(blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children', verbose_name='Categoria padre')
    shop_category = models.ForeignKey(
        ShopCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name='categorie_icecat')

    def create_shop_category(self):
        if ShopCategory.objects.filter(name__iexact=self.name).exists():
            raise CategoryExistsOnShopException()
        elif self.shop_category is not None:
            raise CategoryAlreadyMatchedException()
        else:
            cat = ShopCategory()
            cat.name = self.name

            if self.parent:
                if self.parent.shop_category:
                    cat.parent = self.parent.shop_category

            cat.save()

            self.shop_category = cat
            self.save()
            return True

    def __str__(self) -> str:
        return f"{self.name} ({self.icecat_id})"

    class Meta:
        verbose_name_plural = "categorie"
        verbose_name = "categoria"


class ManufacturerExistsOnShopException(Exception):
    pass


class ManufacturerAlreadyMatchedException(Exception):
    pass


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, blank=False,
                            null=False, verbose_name='Nome')
    icecat_id = models.IntegerField(blank=False, null=False)
    logo_url = models.URLField(blank=True, null=True)
    shop_manufacturer = models.ForeignKey(ShopManufacturer, on_delete=models.SET_NULL, blank=True,
                                          null=True, related_name='marche_icecat', verbose_name='Corrispondenza marca Negozio')

    def __str__(self) -> str:
        return f"{self.name} ({self.icecat_id})"

    def create_shop_manufacturer(self):
        if ShopManufacturer.objects.filter(name__iexact=self.name).exists():
            raise ManufacturerExistsOnShopException()
        elif self.shop_manufacturer is not None:
            raise ManufacturerAlreadyMatchedException()
        else:
            man = ShopManufacturer()
            man.name = self.name
            man.imageUrl = self.logo_url
            man.save()

            self.shop_manufacturer = man
            self.save()
            return True

    class Meta:
        verbose_name_plural = "marche"
        verbose_name = "marca"
