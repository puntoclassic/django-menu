
from decimal import Decimal
from mimetypes import init
from pipes import Template
from typing import Dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from requests import request

from commerce.forms import AddToCartForm, DecreaseQtyForm, IncreaseQtyForm, RemoveFromCartForm

from .models import Category
from .forms import CheckoutConsegnaForm, CheckoutIndirizzoOrarioForm

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

def cart_not_empty(self):
    if self.request.user.is_authenticated:        
        return self.request.session.has_key("cart_items") and len(self.request.session.get("cart_items"))>0
    else:
        return False   

class CheckoutConsegnaView(UserPassesTestMixin,FormView):
    template_name: str = "checkout/consegna.html"   
    form_class = CheckoutConsegnaForm
    tipoConsegna = ""
   
    def get_initial(self):
        initial = super().get_initial()
        initial["tipoConsegna"] = self.request.session.get("checkout_tipoConsegna","domicilio")
        return initial

    def form_valid(self, form):
        self.tipoConsegna = form.cleaned_data["tipoConsegna"]
        self.request.session["checkout_tipoConsegna"] = self.tipoConsegna
        return super().form_valid(form)
    
    def get_success_url(self) -> str:     
        if self.tipoConsegna == 'domicilio':            
            return reverse_lazy('checkout-indirizzo-orario')
        else:
            return reverse_lazy('checkout-riepilogo')     
    
    def test_func(self):
        return cart_not_empty(self)       

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart'))   
    

class CheckoutIndirizzoOrarioView(UserPassesTestMixin,FormView):
    template_name: str = "checkout/indirizzo-orario.html"
    form_class = CheckoutIndirizzoOrarioForm    
    success_url = reverse_lazy("checkout-riepilogo")
   
    def get_initial(self):
        initial = super().get_initial()
        initial["orario"] = self.request.session.get("checkout_orario")
        initial["indirizzo"] = self.request.session.get("checkout_indirizzo")

        print(initial)
        return initial

    def form_valid(self, form):

        self.request.session["checkout_orario"] = form.cleaned_data["orario"]
        self.request.session["checkout_indirizzo"] = form.cleaned_data["indirizzo"]

        return super().form_valid(form)     
    
    def test_func(self):
        return cart_not_empty(self) 

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart'))      

class CheckoutRiepilogoView(UserPassesTestMixin,TemplateView):
    template_name: str = "checkout/riepilogo.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def test_func(self):
        return cart_not_empty(self)   

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart')) 

class CheckoutConfermaView(LoginRequiredMixin,TemplateView):
    template_name: str = "checkout/conferma.html"

