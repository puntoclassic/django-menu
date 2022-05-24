from django.contrib import admin

from icecat.actions import connect_icecat_categories, download_icecat_categories_file, import_icecat_category_selected, import_icecat_category_selected_withchildren, import_icecat_category_selected_withparents, import_icecat_category_withchildren, import_icecat_category_withparents, import_icecat_manufacturers, import_icecat_manufacturers_selected, parse_icecat_categories_file, unzip_icecat_categories_file, create_root_icecat_category
from icecat.filters import ManufacturerHasLogoFilter
from .models import Category, CategoryAlreadyMatchedException, CategoryExistsOnShopException, Manufacturer, ManufacturerAlreadyMatchedException, ManufacturerExistsOnShopException
from django.contrib import messages
from django_object_actions import DjangoObjectActions
from django.utils.html import format_html


@admin.register(Category)
class AdminIcecatCategory(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'icecat_id', 'parent',)
    search_fields = ('name', 'icecat_id',)
    ordering = ['icecat_id', ]
    actions = (import_icecat_category_selected,
               import_icecat_category_selected_withchildren, import_icecat_category_selected_withparents)

    def action_import_category(self, request, obj):
        try:
            obj.create_shop_category()
            messages.add_message(request, messages.SUCCESS,
                                 f"Categoria creata e abbinata")
        except CategoryAlreadyMatchedException:
            messages.add_message(
                request, messages.WARNING, f"Stai provando a creare una categoria che risulta già abbinata")
        except CategoryExistsOnShopException:
            messages.add_message(
                request, messages.WARNING, f"Esiste già una categoria con questo nome {obj.name}")
    action_import_category.label = "Importa categoria"

    # actions
    def action_download_icecat_categories(self, request, obj):
        if download_icecat_categories_file():
            unzip_icecat_categories_file()
            parse_icecat_categories_file()
            create_root_icecat_category()
            connect_icecat_categories()
            messages.add_message(request, messages.SUCCESS,
                                 "Categorie Icecat scaricate con successo")
    action_download_icecat_categories.label = "Scarica"

    def action_import_icecat_category_withchildren(self, request, obj):
        if import_icecat_category_withchildren(obj):
            messages.add_message(request, messages.SUCCESS,
                                 "Categoria con le sue sottocategorie importata")
    action_import_icecat_category_withchildren.label = "Importa categoria con le sue sottocategorie"

    def action_import_icecat_category_withparents(self, request, obj):
        if import_icecat_category_withparents(obj):
            messages.add_message(request, messages.SUCCESS,
                                 "Categoria con le sue categorie superiori importata")
    action_import_icecat_category_withparents.label = "Importa categoria con le sue categorie superiori"

    change_actions = ("action_import_category",
                      "action_import_icecat_category_withchildren", "action_import_icecat_category_withparents")
    changelist_actions = ("action_download_icecat_categories",)


@admin.register(Manufacturer)
class AdminIcecatManufacturer(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('name', 'icecat_id', 'preview_logo',)
    list_filter = (ManufacturerHasLogoFilter,)
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
                                 f"Marca creata e abbinata")
        except ManufacturerAlreadyMatchedException:
            messages.add_message(
                request, messages.WARNING, f"Stai provando a creare una marca che risulta già abbinata")
        except ManufacturerExistsOnShopException:
            messages.add_message(
                request, messages.WARNING, f"Esiste già una marca con questo nome {obj.name}")

    import_manufacturer.label = "Importa marca"

    change_actions = ("import_manufacturer",)

    changelist_actions = ("download_icecat_manufacturers",)
