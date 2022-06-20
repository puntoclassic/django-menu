from django import forms


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
