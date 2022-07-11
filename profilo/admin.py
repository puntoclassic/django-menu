from django.contrib import admin
from .forms import *
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from copy import deepcopy

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    form = CustomUserChangeForm
    list_display = ('first_name', 'last_name',
                    'email')
    list_display_links = ('first_name','last_name','email')   

    

   
