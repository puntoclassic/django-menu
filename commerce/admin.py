from django.contrib import admin
from commerce.actions import manufacturers_download_logo
from django_object_actions import DjangoObjectActions
from commerce.forms import CustomSignInForm, CustomUserChangeForm

from commerce.models import Category, CommerceUser, Manufacturer
from mptt.admin import MPTTModelAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(Category)
class AdminCategory(MPTTModelAdmin):
    list_display = ('name','slug',)

@admin.register(Manufacturer)
class AdminManufacturer(DjangoObjectActions, admin.ModelAdmin):
    actions = (manufacturers_download_logo,)

    def download_logo(self,request,obj):
        if obj.imageUrl is not None and obj.imageUrl != "":
            obj.download_logo()
        else:
            self.message_user()
    download_logo.label = "Scarica logo"  

    change_actions = ('download_logo', )


@admin.register(CommerceUser)
class CustomUserAdmin(UserAdmin): 
    add_form = CustomSignInForm
    form = CustomUserChangeForm 
    model = CommerceUser

    fieldsets = UserAdmin.fieldsets + (
            ('Informazioni cliente', {'fields': ('tipologia',)}),
    )
