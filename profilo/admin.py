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
                    'email','email_verified')
    list_display_links = ('first_name','last_name','email')  

    def get_fieldsets(self, request, obj):
        fieldsets = deepcopy(super().get_fieldsets(request, obj))
        fieldsets[1][1]["fields"] += ("email_verified",'activation_code',)
        return fieldsets 

   

    

   
