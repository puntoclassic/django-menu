from pyexpat import model
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User

class CustomUserChangeForm(UserChangeForm):
    email_verified = forms.BooleanField(label="Email verificata",required=False)

    class Meta:
        model = User
        fields = "__all__"
        
    
        