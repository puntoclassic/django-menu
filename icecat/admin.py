import gzip
from hashlib import new
from django.contrib import admin

from commerce.models import Category, Manufacturer
from .models import IcecatCategory, IcecatManufacturer, IcecatManufacturerAlreadyMatchedException, IcecatManufacturerExistsOnShopException
from mptt.admin import MPTTModelAdmin
from django.contrib import messages
from django_object_actions import DjangoObjectActions
from shop.settings import BASE_DIR, env
import requests
import xml.etree.ElementTree as ET
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
import os

# Register your models here.
@admin.register(IcecatCategory)
class AdminIcecatCategory(MPTTModelAdmin):
    pass

class IcecatManufacturerHasLogoFilter(SimpleListFilter):
    title = 'Marche con logo' 
    parameter_name = 'hasLogoUrl'

    def lookups(self, request, model_admin):
        return [
            ("yes", "Si"),
            ("no", "No"),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(logo_url__iexact="")
        if self.value():
            return queryset.filter(logo_url__iexact="")

@admin.register(IcecatManufacturer)
class AdminIcecatManufacturer(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name','icecat_id','preview_logo',)
    list_filter = (IcecatManufacturerHasLogoFilter,)
    search_fields = ('name','icecat_id',)

    @admin.display(description="Preview Logo")
    def preview_logo(self,obj):
        if obj.logo_url != "":
            return format_html(f"""
            <div>
                <img src='{obj.logo_url}' height="32"/>            
            </div>
            """)
        else:
            return "Nessun url per il logo disponibile"
    preview_logo.allow_tags=True
    
    #actions
    def download_icecat_manufacturer(self, request, obj):
        username = env("ICECAT_USERNAME")
        password = env("ICECAT_PASSWORD")
        link = f"https://{username}:{password}@data.icecat.biz/export/freexml.int/refs/SuppliersList.xml.gz"
        path_gz = f"{BASE_DIR}/external_data/SuppliersList.xml.gz"
        xml_path = f"{BASE_DIR}/external_data/SuppliersList.xml"
        content = requests.get(link).content
        if content:
            file_gz = open(path_gz,"wb")
            file_gz.write(content)
            file_gz  = gzip.open(path_gz,"rb")
            
            file_xml = open(xml_path,"wb")
            file_xml.write(file_gz.read())
            file_xml.close()   

            tree = ET.parse(xml_path)
            root = tree.getroot()

            for supplier in root.iter('Supplier'):
               if IcecatManufacturer.objects.filter(icecat_id=supplier.attrib["ID"]).count() == 0:
                   new_man = IcecatManufacturer()
                   new_man.icecat_id = supplier.attrib["ID"]
                   new_man.name = supplier.attrib["Name"]
                   new_man.logo_url = supplier.attrib["LogoMediumPic"]
                   new_man.save()
            os.remove(path_gz)
            messages.add_message(request,messages.SUCCESS,"Marche Icecat scaricate con successo")        
    download_icecat_manufacturer.label = "Scarica"

    def import_manufacturer(self, request, obj):
        try:
            obj.create_shop_manufacturer()
            messages.add_message(request,messages.SUCCESS,f"Categoria creata e abbinata") 
        except IcecatManufacturerAlreadyMatchedException:
            messages.add_message(request,messages.WARNING,f"Stai provando a creare una marca che risulta già abbinata")  
        except IcecatManufacturerExistsOnShopException:
            messages.add_message(request,messages.WARNING,f"Esiste già una marca con questo nome {obj.name}")  
             
    import_manufacturer.label = "Importa marca"

    change_actions = ("import_manufacturer",)

    changelist_actions = ("download_icecat_manufacturer",)

 
    