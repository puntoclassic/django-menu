from django.contrib import admin
from .models import IcecatCategory, IcecatManufacturer
from mptt.admin import MPTTModelAdmin

# Register your models here.
@admin.register(IcecatCategory)
class AdminIcecatCategory(MPTTModelAdmin):
    pass

@admin.register(IcecatManufacturer)
class AdminIcecatManufacturer(admin.ModelAdmin):
    pass