from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, PasswordResetForm, UserChangeForm
from django import forms

from commerce.models import CommerceUser


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,"class":'form-control'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class":'form-control'}),
    )

class CustomSignInForm(UserCreationForm):   
    error_css_class = "is-invalid"
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,"class":'form-control'}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),       
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class":"form-control"}),
        strip=False,        
    )
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":'form-control'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":'form-control'}))
    tipologia = forms.ChoiceField(required=True,choices=[
        ('PRIVATO','Privato'),
        ('AZIENDA','Azienda'),
        ('PUBBLICA_AMMINISTRAZIONE','Pubblica Amministrazione'),
        ('ASSOCIAZIONE','Associazione')
    ],widget=forms.Select(attrs={"class":'form-control'}))

    class Meta(UserCreationForm):
        model = CommerceUser
        fields = UserCreationForm.Meta.fields + ('tipologia',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

class CustomPasswordRecoveryForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email", 
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email","class":"form-control"}),
    )

class ContactForm(forms.Form):
    first_name = forms.CharField(label="Nome",disabled=True,required=True,widget=forms.TextInput(attrs={"class":'form-control'}))
    last_name = forms.CharField(label="Cognome",disabled=True,required=True,widget=forms.TextInput(attrs={"class":'form-control'}))
    email = forms.EmailField(
        label="Email", 
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email","class":"form-control"}),
    )
    corpo =  forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}),)



class CustomUserChangeForm(UserChangeForm):   
    class Meta:
        model = CommerceUser
        fields = UserChangeForm.Meta.fields