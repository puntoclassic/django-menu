from django.contrib import admin

from .models import ImpostazioniGenerali, ImpostazioniOrdini, ImpostazioniSpedizione,User
from solo.admin import SingletonModelAdmin
# Register your models here.
from allauth.account.models import EmailAddress
from django.contrib.auth.admin import UserAdmin 


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name',
                    'email','email_verified')
    list_display_links = ('first_name','last_name','email')  

    @admin.display(description='Email verificata',boolean=True)
    def email_verified(self,obj):
        return obj.verified

@admin.register(ImpostazioniGenerali)
class AdminImpostazioniGenerali(SingletonModelAdmin):
    pass

@admin.register(ImpostazioniSpedizione)
class AdminImpostazioniConsegna(SingletonModelAdmin):
    pass

@admin.register(ImpostazioniOrdini)
class AdminImpostazioniOrdini(SingletonModelAdmin):
    pass