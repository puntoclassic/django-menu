
from decimal import Decimal
from typing import Dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView


from django.contrib.auth.mixins import LoginRequiredMixin

from commerce.forms import AddToCartForm, DecreaseQtyForm, IncreaseQtyForm, RemoveFromCartForm

from .models import Category

# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"


class ErrorPageView(TemplateView):
    template_name = "error.html"


class CategoriaListView(DetailView):
    template_name = "categoria.html"
    model = Category

    def get_object(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.model.objects.filter(slug=self.kwargs['slug']).first()

# profile views


class CartView(TemplateView):
    template_name: str = "carrello.html"


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)

        if form.is_valid():
            cart_items = request.session.get('cart_items', {})
            cart_amount = Decimal(0.00)

            if form.cleaned_data["food_id"] in cart_items.keys():
                cart_items[form.cleaned_data["food_id"]]["quantity"] += 1
            else:
                cart_items[form.cleaned_data["food_id"]] = {
                    "id": form.cleaned_data["food_id"],
                    "name": form.cleaned_data["food_name"],
                    "quantity": 1,
                    "price": str(form.cleaned_data["food_price"])
                }

            for item in cart_items.values():
                cart_amount += Decimal(item["price"]) * item["quantity"]

            request.session["cart_items"] = cart_items
            request.session["cart_amount"] = str(cart_amount)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        form = RemoveFromCartForm(request.POST)

        if form.is_valid():
            cart_items: Dict = request.session.get('cart_items', {})
            cart_amount = Decimal(0.00)

            row_id = str(form.cleaned_data["food_id"])
            del cart_items[row_id]

            for item in cart_items.values():
                cart_amount += Decimal(item["price"]) * item["quantity"]

            request.session["cart_items"] = cart_items
            request.session["cart_amount"] = str(cart_amount)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class IncreaseQtyView(View):
    def post(self, request, *args, **kwargs):
        form = IncreaseQtyForm(request.POST)

        if form.is_valid():
            cart_items: Dict = request.session.get('cart_items', {})
            cart_amount = Decimal(0.00)

            row_id = str(form.cleaned_data["food_id"])

            cart_items[row_id]["quantity"] += 1

            for item in cart_items.values():
                cart_amount += Decimal(item["price"]) * item["quantity"]

            request.session["cart_items"] = cart_items
            request.session["cart_amount"] = str(cart_amount)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DecreaseQtyView(View):
    def post(self, request, *args, **kwargs):
        form = DecreaseQtyForm(request.POST)

        if form.is_valid():
            cart_items = request.session.get('cart_items', {})
            cart_amount = Decimal(0.00)

            row_id = str(form.cleaned_data["food_id"])

            if cart_items[row_id]["quantity"] == 1:
                del cart_items[row_id]
            else:
                cart_items[row_id]["quantity"] -= 1

            for item in cart_items.values():
                cart_amount += Decimal(item["price"]) * item["quantity"]

            request.session["cart_items"] = cart_items
            request.session["cart_amount"] = str(cart_amount)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
