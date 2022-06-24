from django import forms
from pkg_resources import require


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
    tipoConsegna = forms.ChoiceField(required=True,choices=[
        ('domicilio',"Consegna a domicilio 2 €"),
        ('asporto','Ritiro in negozio',)
    ],widget=forms.Select(attrs={'class':"form-control"}))

class CheckoutIndirizzoOrarioForm(forms.Form):
    indirizzo = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))
    orario = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))

class CheckoutRiepilogoOrdineForm(forms.Form):
    note = forms.CharField(required=False)