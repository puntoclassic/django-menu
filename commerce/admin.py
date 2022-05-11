from django.contrib import admin
from commerce.actions import manufacturers_download_logo

from commerce.models import Category, Manufacturer
from mptt.admin import MPTTModelAdmin


# Register your models here.
@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ('name','slug',)

@admin.register(Manufacturer)
class AdminManufacturer(admin.ModelAdmin):
    actions = (manufacturers_download_logo,)

    def download_logo(self,obj):
        if obj.imageUrl is not None and obj.imageUrl != "":
            obj.download_picture()
        else:
            self.message_user()
    download_logo.label = "Scarica logo"  

    change_actions = ('download_logo', )
