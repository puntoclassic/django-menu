from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User

class CustomUserChangeForm(UserChangeForm):
    email_verified = forms.BooleanField(label="Email verificata",required=False)
    activation_code = forms.CharField(label="Codice di attivazione",required=False)


    class Meta:
        model = User
        fields = "__all__" 
