from django.contrib import admin
from .forms import *
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomSignInForm
    form = CustomUserChangeForm
    model = User

    list_display = ('first_name', 'last_name',
                    'email', 'is_staff',)
    list_display_links = ('first_name','last_name','email')

    fieldsets = UserAdmin.fieldsets 
