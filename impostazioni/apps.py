from django.apps import AppConfig
from allauth.account.signals import email_confirmed


class ImpostazioniConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'impostazioni'

    def ready(self) -> None:
        email_confirmed.connect(self.email_confirmed_receiver)
        return super().ready()
    
    def email_confirmed_receiver(*args, **kwargs):
        from .models import User

        emailAddress = kwargs["email_address"]
        user = User.objects.filter(email=emailAddress.email).first()
        user.email_verified = True
        user.save()
