from django.contrib import admin, messages
from commerce.actions import categories_update_slug, manufacturers_download_logo
from django_object_actions import DjangoObjectActions
from commerce.forms import CustomSignInForm, CustomUserChangeForm

from commerce.models import Category, CommerceUser, Manufacturer, Product
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

'''
@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ('name', 'slug',)
    actions = (categories_update_slug,)


@admin.register(Manufacturer)
class AdminManufacturer(DjangoObjectActions, admin.ModelAdmin):
    actions = (manufacturers_download_logo,)

    # download the logo from url
    def download_logo(self, request, obj):
        if obj.download_logo():
            messages.success(
                request, "Immagine logo scaricata con successo")
        else:
            messages.warning(
                request, "Non è stato possibile scaricare l'immagine, url potrebbe essere vuoto oppure errato")

    download_logo.label = "Scarica logo"

    change_actions = ('download_logo', )

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    pass

@admin.register(CommerceUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomSignInForm
    form = CustomUserChangeForm
    model = CommerceUser

    list_display = ('first_name', 'last_name',
                    'email', 'tipologia', 'is_staff',)

    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni cliente', {'fields': ('tipologia',)}),
    )
'''