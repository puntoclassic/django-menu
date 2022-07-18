from django import forms

from impostazioni.models import ImpostazioniSpedizione

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

class CassaConsegnaForm(forms.Form): 

    tipo_consegna = forms.ChoiceField(required=True,choices=[
        ('domicilio',f"Consegna a domicilio €"),
        ('asporto','Ritiro in negozio',)
    ],widget=forms.Select(attrs={'class':"form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_consegna'] = forms.ChoiceField(required=True,choices=[
        ('domicilio',f"Consegna a domicilio {ImpostazioniSpedizione.get_solo().shipping_costs} €"),
        ('asporto','Ritiro in negozio',)
    ],widget=forms.Select(attrs={'class':"form-control"}))


    



   

class CassaIndirizzoOrarioForm(forms.Form):
    error_css_class = "is-invalid" 
    use_required_attribute: bool = False           
    indirizzo = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))
    orario = forms.CharField(required=True,widget=forms.TextInput(attrs={"class":"form-control"}))   

class CassaRiepilogoOrdineForm(forms.Form):
    note = forms.CharField(required=False)


