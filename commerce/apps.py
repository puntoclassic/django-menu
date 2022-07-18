from django.apps import AppConfig
from allauth.account.signals import email_confirmed


class CommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'commerce'

    
