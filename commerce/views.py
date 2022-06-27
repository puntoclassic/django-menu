
from decimal import Decimal
from pipes import Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string, get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from requests import request
import stripe


from commerce.forms import AddToCartForm, DecreaseQtyForm, IncreaseQtyForm, RemoveFromCartForm
from impostazioni.models import GeneraliModel
from shop.settings import EMAIL_FROM_NAME, EMAIL_HOST_USER, env

from .models import Category, Order, OrderDetail, OrderStatus
from .forms import CheckoutConsegnaForm, CheckoutIndirizzoOrarioForm, CheckoutRiepilogoOrdineForm

# Create your views here.
stripe.api_key = env("STRIPE_TEST_SECRET_KEY")

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
            cart = get_cart(request)            
            cart["amount"] = Decimal(0.00)

            if form.cleaned_data["food_id"] in cart["items"].keys():
                cart["items"][form.cleaned_data["food_id"]]["quantity"] += 1
            else:
                cart["items"][form.cleaned_data["food_id"]] = {
                    "id": form.cleaned_data["food_id"],
                    "name": form.cleaned_data["food_name"],
                    "quantity": 1,
                    "price": str(form.cleaned_data["food_price"])
                }

            for item in cart["items"].values():
                cart["amount"] += Decimal(item["price"]) * item["quantity"]
            cart["amount"] =str(cart["amount"])
            request.session["cart"] = cart

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveFromCartView(View):
    def post(self, request, *args, **kwargs):
        form = RemoveFromCartForm(request.POST)

        if form.is_valid():          

            cart = get_cart(request)
            row_id = str(form.cleaned_data["food_id"])
            del cart["items"][row_id]

            cart["amount"] = Decimal(0.00)

            for item in cart["items"].values():
                cart["amount"] += Decimal(item["price"]) * item["quantity"]
            cart["amount"] =str(cart["amount"])
            request.session["cart"] = cart
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class IncreaseQtyView(View):
    def post(self, request, *args, **kwargs):
        form = IncreaseQtyForm(request.POST)

        if form.is_valid():

            cart = get_cart(request)
            row_id = str(form.cleaned_data["food_id"])

            cart["items"][row_id]["quantity"] += 1
            cart["amount"] = Decimal(0.00)

            for item in cart["items"].values():
                cart["amount"] += Decimal(item["price"]) * item["quantity"]

            cart["amount"] =str(cart["amount"])
            request.session["cart"] = cart
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DecreaseQtyView(View):
    def post(self, request, *args, **kwargs):
        form = DecreaseQtyForm(request.POST)

        if form.is_valid():
            cart = get_cart(request)

            row_id = str(form.cleaned_data["food_id"])

            if cart["items"][row_id]["quantity"] == 1:
                del cart["items"][row_id]
            else:
                cart["items"][row_id]["quantity"] -= 1

            for item in cart["items"].values():
                cart["amount"] += Decimal(item["price"]) * item["quantity"]
            
            cart["amount"] =str(cart["amount"])

            request.session["cart"] = cart
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart_not_empty(self):
    if self.request.user.is_authenticated:        
        return self.request.session.has_key("cart") and len(self.request.session.get("cart")["items"])>0
    else:
        return False   

def get_cart(request):
    return request.session.get("cart",{
                "items":{},
                "amount":"",
                "tipoConsegna":"domicilio",
                "orario":"",
                "indirizzo":"",                
            })

class CheckoutConsegnaView(UserPassesTestMixin,FormView):
    template_name: str = "checkout/consegna.html"   
    form_class = CheckoutConsegnaForm
    cart = None
   
    def get_initial(self):
        initial = super().get_initial()
        self.cart = get_cart(self.request)
        initial["tipoConsegna"] = self.cart["tipoConsegna"]
        return initial

    def form_valid(self, form):
        self.cart["tipoConsegna"] = form.cleaned_data["tipoConsegna"]        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:     
        self.request.session["cart"] = self.cart
        if self.cart["tipoConsegna"] == 'domicilio':            
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
    cart = None
   
    def get_initial(self):
        initial = super().get_initial()
        self.cart = get_cart(self.request)
        initial["orario"] = self.cart["orario"]
        initial["indirizzo"] = self.cart["indirizzo"]
        return initial

    def form_valid(self, form):
        
        self.cart["orario"] = form.cleaned_data["orario"]
        self.cart["indirizzo"] = form.cleaned_data["indirizzo"]
        self.request.session["cart"] = self.cart

        return super().form_valid(form)     
    
    def test_func(self):
        return cart_not_empty(self) 

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart'))      

class CheckoutRiepilogoView(UserPassesTestMixin,FormView):
    template_name: str = "checkout/riepilogo.html"  

    form_class = CheckoutRiepilogoOrdineForm
    ordine = Order()
    
    def form_valid(self, form):
        cart = get_cart(self.request)
        note = form.cleaned_data["note"]        
        self.ordine.customer = self.request.user
        self.ordine.note = note
        self.ordine.shippingAddress = cart["indirizzo"]
        self.ordine.shippingDeliveryTime = cart["orario"]
        self.ordine.shippingRequired = True if cart["tipoConsegna"] == "domicilio" else False
        self.ordine.shippingCosts = 2.00 if cart["tipoConsegna"] == "domicilio" else 0.00
        self.ordine.subTotal = Decimal(cart["amount"])+Decimal(self.ordine.shippingCosts)
        self.ordine.orderStatus = OrderStatus.objects.filter(description="Ordine creato").first()
        self.ordine.save()  

        if self.ordine.shippingRequired:
            order_row = OrderDetail()
            order_row.order = self.ordine
            order_row.name = "Spese di consegna"
            order_row.price = Decimal(self.ordine.shippingCosts)
            order_row.quantity = 1
            order_row.save()


        items = self.request.session["cart"]["items"] 
        for item in items.values():
            order_row = OrderDetail()
            order_row.order = self.ordine
            order_row.name = item["name"]
            order_row.price = Decimal(item["price"])
            order_row.quantity = item["quantity"]
            order_row.save()    



        del self.request.session["cart"]        

        return super().form_valid(form)


    def get_success_url(self) -> str:
        return reverse("checkout-conferma",kwargs={"id":self.ordine.id})

    def test_func(self):
        return cart_not_empty(self)   

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart')) 

class CheckoutConfermaView(UserPassesTestMixin,TemplateView):
    template_name: str = "checkout/conferma.html"  

    def test_func(self):
        if self.request.user.is_authenticated:
            order_id = self.kwargs["id"]  
           
            order = Order.objects.filter(id=order_id).first()
            if order.customer.id==self.request.user.id:
                return True           
            return False
        else:
            return False    

    def get(self, request, *args, **kwargs):
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data  =super().get_context_data(**kwargs)
        context_data["order_id"] = kwargs.get("id")

        message = get_template('account/email/email_order_created.html').render({
             "base_info": GeneraliModel.get_solo(),
            "order_id":kwargs.get("id")
        })
 
        #send_mail("Il tuo ordine è stato creato",message,from_email=EMAIL_HOST_USER,recipient_list=[self.request.user.email],html_message=message)
        return context_data

class CheckoutPagaView(UserPassesTestMixin,TemplateView):
    template_name: str = "checkout/paga.html"

    def get_context_data(self, **kwargs):
        """
        Creates and returns a Stripe Checkout Session
        """
        # Get Parent Context
        context = super().get_context_data(**kwargs)

        # to initialise Stripe.js on the front end
        context[
            "STRIPE_PUBLIC_KEY"
        ] = env("STRIPE_PUBLIC_KEY")

        success_url = self.request.build_absolute_uri(
            reverse("checkout-pagato",kwargs={"id":kwargs["id"]})
        )
        cancel_url = self.request.build_absolute_uri(reverse("home"))                 


        order_lines = OrderDetail.objects.filter(order_id=kwargs["id"]).all()

        order_items = []

        for line in order_lines:
            order_items.append(
                    {
                        "price_data": {
                            "currency": "eur",
                            "unit_amount": int(line.price*100),
                            "product_data": {
                                "name": line.name,                               
                            },
                        },
                        "quantity": line.quantity,
                    },                
            )

        session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                payment_intent_data={
                    "setup_future_usage": "off_session",                   
                },
                line_items=order_items,
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    "order_sku":kwargs["id"]
                }
            )           

        context["CHECKOUT_SESSION_ID"] = session.id

        return context

    def test_func(self):
        if self.request.user.is_authenticated:
            order_id = self.kwargs["id"]  
           
            order = Order.objects.filter(id=order_id).first()
            if order.customer.id==self.request.user.id:
                return True           
            return False
        else:
            return False  

class CheckoutPagatoView(UserPassesTestMixin,TemplateView):
    template_name: str = "checkout/pagato.html"

    def test_func(self):
        if self.request.user.is_authenticated:
            order_id = self.kwargs["id"]  
           
            order = Order.objects.filter(id=order_id).first()
            if order.customer.id==self.request.user.id:
                return True           
            return False
        else:
            return False  



from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = env('STRIPE_TEST_SECRET_KEY')
    endpoint_secret = env('STRIPE_ENDPOINT_SECRET')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        metadata = event["data"]["object"]['metadata']   
        order = Order.objects.filter(id=metadata["order_sku"]).first()
        order.payed = True
        order.save()    
    return HttpResponse(status=200)