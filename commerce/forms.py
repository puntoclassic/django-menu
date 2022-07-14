from django import forms
from .models import User

from django.contrib.auth.forms import UsernameField, UserCreationForm, PasswordResetForm, UserChangeForm
from allauth.account.forms import LoginForm, SignupForm


class AddToCartForm(forms.Form):
    food_id = forms.IntegerField(required=True)
    food_name = forms.CharField(required=True)
    food_price = forms.DecimalField(
        localize=True,
        required=True, decimal_places=2, max_digits=6)


class IncreaseQtyForm(forms.Form):
    food_id = forms.IntegerField(required=True)


class DecreaseQtyForm(forms.Form):
    food_id = forms.IntegerField(required=True)


class RemoveFromCartForm(forms.Form):
    food_id = forms.IntegerField(required=True)

class CheckoutConsegnaForm(forms.Form): 

    tipo_consegna = forms.ChoiceField(required=True,choices=[
        ('domicilio',"Consegna a domicilio 2 €"),
        ('asporto','Ritiro in negozio',)
    ],widget=forms.Select(attrs={'class':"form-control"}))

   

class CheckoutIndirizzoOrarioForm(forms.Form):
    error_css_class = "is-invalid" 
    use_required_attribute: bool = False           
    indirizzo = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))
    orario = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))   

class CheckoutRiepilogoOrdineForm(forms.Form):
    note = forms.CharField(required=False)


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


class ContactForm(forms.Form):
    first_name = forms.CharField(label="Nome", disabled=True, required=True,
                                 widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label="Cognome", disabled=True, required=True,
                                widget=forms.TextInput(attrs={"class": 'form-control'}))
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "class": "form-control"}),
    )
    corpo = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control"}),)

    
class AccountInformazioniEditForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", disabled=False, required=True,
                                 widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(label="Cognome", disabled=False, required=True,
                                widget=forms.TextInput(attrs={"class": 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)
