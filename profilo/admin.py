from django.contrib import admin
from .forms import *
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from copy import deepcopy
from allauth.account.models import EmailAddress

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name',
                    'email','email_verified')
    list_display_links = ('first_name','last_name','email')  

    @admin.display(description='Email verificata',boolean=True)
    def email_verified(self,obj):
        return EmailAddress.objects.filter(email=obj.email).first().verified

   

    

   
