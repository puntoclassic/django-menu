from django.contrib import admin, messages
from commerce.actions import categories_update_slug
from django_object_actions import DjangoObjectActions
from commerce.forms import CustomSignInForm, CustomUserChangeForm

from commerce.models import Category, CommerceUser, Food
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    actions = (categories_update_slug,)


@admin.register(Food)
class AdminFood(admin.ModelAdmin):
    pass

@admin.register(CommerceUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomSignInForm
    form = CustomUserChangeForm
    model = CommerceUser

    list_display = ('first_name', 'last_name',
                    'email', 'tipologia', 'is_staff',)

    list_display_links = ('first_name','last_name','email')

    fieldsets = UserAdmin.fieldsets + (
        ('Informazioni cliente', {'fields': ('tipologia',)}),
    )
