
from decimal import Decimal
from mimetypes import init
from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.template.loader import get_template
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from impostazioni.models import ImpostazioniGenerali, ImpostazioniSpedizione


from .forms import AddToCartForm, DecreaseQtyForm, IncreaseQtyForm, RemoveFromCartForm
from shop.settings import EMAIL_HOST_USER, env

from .models import Order, OrderDetail, OrderStatus
from .forms import CassaConsegnaForm, CassaIndirizzoOrarioForm, CassaRiepilogoOrdineForm


# Create your views here.
stripe.api_key = env("STRIPE_TEST_SECRET_KEY")



class CartView(TemplateView):
    template_name: str = "vendite/carrello.html"


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

            cart["amount"] = Decimal(0.00)

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
                "tipo_consegna":"domicilio",
                "orario":"",
                "indirizzo":"",                
            })

class CassaConsegnaView(UserPassesTestMixin,FormView):
    template_name: str = "vendite/cassa/consegna.html"   
    form_class = CassaConsegnaForm
    cart = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shipping_costs"] = ImpostazioniSpedizione.get_solo().shipping_costs
        return context
   
    def get_initial(self):
        initial = super().get_initial()        
        self.cart = get_cart(self.request)       
       
        initial["tipo_consegna"] = self.cart["tipo_consegna"] 
        return initial

    def form_valid(self, form):
        self.cart["tipo_consegna"] = form.cleaned_data["tipo_consegna"]        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:     
        self.request.session["cart"] = self.cart
        if self.cart["tipo_consegna"] == 'domicilio':            
            return reverse_lazy('vendite.cassa.indirizzo.orario')
        else:
            return reverse_lazy('vendite.cassa.riepilogo')     
    
    def test_func(self):
        return cart_not_empty(self)       

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('vendite.carrello'))   
    

class CassaIndirizzoOrarioView(UserPassesTestMixin,FormView):
    template_name: str = "vendite/cassa/indirizzo_orario.html"
    form_class = CassaIndirizzoOrarioForm    
    success_url = reverse_lazy("vendite.cassa.riepilogo")
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
        return redirect(reverse_lazy('vendite.carrello'))      

class CassaRiepilogoView(UserPassesTestMixin,FormView):
    template_name: str = "vendite/cassa/riepilogo.html"  

    form_class = CassaRiepilogoOrdineForm
    order = Order()

    def get_context_data(self, **kwargs) :
        context_data = super().get_context_data(**kwargs)
        impostazioni = ImpostazioniSpedizione.get_solo()

        context_data["shipping_costs"] = impostazioni.shipping_costs
        return context_data    
    
    def form_valid(self, form):
        impostazioni = ImpostazioniSpedizione.get_solo()
        cart = get_cart(self.request)
        note = form.cleaned_data["note"]        
        self.order.customer = self.request.user
        self.order.note = note
        self.order.shipping_address = cart["indirizzo"]
        self.order.shipping_delivery_time = cart["orario"]
        self.order.shipping_required = True if cart["tipo_consegna"] == "domicilio" else False
        self.order.shipping_costs = impostazioni.shipping_costs if cart["tipo_consegna"] == "domicilio" else 0.00
        self.order.order_status = OrderStatus.objects.filter(description="Creato").first()
        self.order.save()  

        if self.order.shipping_required == True:
            order_row = OrderDetail()
            order_row.order = self.order
            order_row.name = "Spese di consegna"
            order_row.unit_price = Decimal(impostazioni.shipping_costs)
            order_row.quantity = 1
            order_row.save()


        items = self.request.session["cart"]["items"] 
        for item in items.values():
            order_row = OrderDetail()
            order_row.order = self.order
            order_row.name = item["name"]
            order_row.unit_price = Decimal(item["price"])
            order_row.quantity = item["quantity"]
            order_row.save()    



        del self.request.session["cart"]    

        message = get_template('vendite/email/email_order_created.html').render({
            "base_info": ImpostazioniGenerali.get_solo(),
            "order":self.order            
        })
 
        send_mail("Il tuo ordine è stato creato",message,from_email=EMAIL_HOST_USER,recipient_list=[self.request.user.email],html_message=message)   
 

        return super().form_valid(form)


    def get_success_url(self) -> str:
        messages.add_message(self.request,messages.SUCCESS,"Il tuo ordine è stato confermato","profilo-ordini")        
        return reverse('vendite.ordine.dettaglio',kwargs={"pk":self.order.id})

    def test_func(self):
        return cart_not_empty(self)   

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('vendite.carrello'))       

   

class CassaPagaView(UserPassesTestMixin,TemplateView):
    template_name: str = "vendite/cassa/paga.html"

    def get_context_data(self, **kwargs):
        """
        Creates and returns a Stripe Cassa Session
        """
        # Get Parent Context
        context = super().get_context_data(**kwargs)

        # to initialise Stripe.js on the front end
        context[
            "STRIPE_PUBLIC_KEY"
        ] = env("STRIPE_PUBLIC_KEY")

        success_url = self.request.build_absolute_uri(
            reverse("vendite.ordine.pagato",kwargs={"id":kwargs["id"]})
        )
        cancel_url = self.request.build_absolute_uri(reverse("home"))                 


        order_lines = OrderDetail.objects.filter(order_id=kwargs["id"]).all()

        order_items = []

        for line in order_lines:
            order_items.append(
                    {
                        "price_data": {
                            "currency": "eur",
                            "unit_amount": int(line.unit_price*100),
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

class CassaPagatoView(UserPassesTestMixin,TemplateView):
    template_name: str = "vendite/cassa/pagato.html"

    def test_func(self):
        if self.request.user.is_authenticated:
            order_id = self.kwargs["id"]  
           
            order = Order.objects.filter(id=order_id).first()
            if order.customer.id==self.request.user.id:
                return True           
            return False
        else:
            return False  

    def get(self, request, *args, **kwargs) -> HttpResponse:
        messages.add_message(request,messages.SUCCESS,"Hai pagato il tuo ordine","profilo-ordini")
        return redirect(reverse('vendite.ordine.dettaglio',kwargs={"pk":kwargs.get("id")}))

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
    

    # Handle the Cassa.session.completed event
    if event['type'] == 'checkout.session.completed':
        metadata = event["data"]["object"]['metadata']   
        order = Order.objects.filter(id=metadata["order_sku"]).first()
        order.order_status = OrderStatus.objects.filter(description="Pagato").first()
        order.is_paid = True
        order.save()   

        message = get_template('vendite/email/email_order_paid.html').render({
            "base_info": ImpostazioniGenerali.get_solo(),
            "order":order
        }) 
        send_mail("Il tuo ordine è stato pagato",message,from_email=EMAIL_HOST_USER,recipient_list=[order.customer.email],html_message=message)

    return HttpResponse(status=200)


class OrderListView(ListView):
    model = Order
    template_name = "vendite/ordine/list_view.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(customer=self.request.user)
        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = "vendite/ordine/detail_view.html"    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)