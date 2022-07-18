from django import forms
from .models import User

from django.contrib.auth.forms import UsernameField, UserCreationForm, PasswordResetForm
from allauth.account.forms import LoginForm, SignupForm

class CustomLoginForm(LoginForm):
    login = UsernameField(widget=forms.TextInput(
        attrs={"autofocus": True, "class": 'form-control'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": 'form-control'}),
    )

class CustomSignInForm(SignupForm):
    email =forms.EmailField(widget=forms.TextInput(
        attrs={"autofocus": True, "class": 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
    )
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields

    def save(self, request):
        user = super().save(request)
        user.email = self.cleaned_data["email"]
        user.username = user.email
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]        
        return user


class CustomPasswordRecoveryForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}),
    )

    
class AccountInformazioniEditForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", disabled=False, required=True,
                                 widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label="Cognome", disabled=False, required=True,
                                widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
