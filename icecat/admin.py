import gzip
from hashlib import new
from django.contrib import admin

from commerce.models import Category, Manufacturer
from icecat.actions import connect_icecat_categories, download_icecat_categories_file, import_icecat_manufacturers, import_icecat_manufacturers_selected, parse_icecat_categories_file, unzip_icecat_categories_file, create_root_icecat_category
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
class AdminIcecatCategory(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'icecat_id', 'parent',)
    search_fields = ('name', 'icecat_id',)
    ordering = ['icecat_id', ]

    # actions
    def download_icecat_categories(self, request, obj):
        if download_icecat_categories_file():
            unzip_icecat_categories_file()
            parse_icecat_categories_file()
            create_root_icecat_category()
            connect_icecat_categories()
            messages.add_message(request, messages.SUCCESS,
                                 "Categorie Icecat scaricate con successo")

    download_icecat_categories.label = "Scarica"
    changelist_actions = ("download_icecat_categories",)


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
    list_display = ('name', 'icecat_id', 'preview_logo',)
    list_filter = (IcecatManufacturerHasLogoFilter,)
    search_fields = ('name', 'icecat_id',)
    actions = (import_icecat_manufacturers_selected,)

    @admin.display(description="Preview Logo")
    def preview_logo(self, obj):
        if obj.logo_url != "":
            return format_html(f"""
            <div>
                <img src='{obj.logo_url}' height="32"/>            
            </div>
            """)
        else:
            return "Nessun url per il logo disponibile"
    preview_logo.allow_tags = True

    # actions
    def download_icecat_manufacturers(self, request, obj):
        if import_icecat_manufacturers():
            messages.add_message(request, messages.SUCCESS,
                                 "Marche Icecat scaricate con successo")
    download_icecat_manufacturers.label = "Scarica"

    def import_manufacturer(self, request, obj):
        try:
            obj.create_shop_manufacturer()
            messages.add_message(request, messages.SUCCESS,
                                 f"Categoria creata e abbinata")
        except IcecatManufacturerAlreadyMatchedException:
            messages.add_message(
                request, messages.WARNING, f"Stai provando a creare una marca che risulta già abbinata")
        except IcecatManufacturerExistsOnShopException:
            messages.add_message(
                request, messages.WARNING, f"Esiste già una marca con questo nome {obj.name}")

    import_manufacturer.label = "Importa marca"

    change_actions = ("import_manufacturer",)

    changelist_actions = ("download_icecat_manufacturers",)
