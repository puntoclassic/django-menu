
from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import UserPassesTestMixin

from django.template.loader import get_template
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.mail import send_mail


from impostazioni.models import GeneraliModel
from shop.settings import EMAIL_HOST_USER, env

from .models import Order

# Create your views here.
stripe.api_key = env("STRIPE_TEST_SECRET_KEY")

class HomeView(TemplateView):
    template_name = "index.html"

class ErrorPageView(TemplateView):
    template_name = "error.html"
       

'''
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
        order = Order.objects.filter(id=kwargs.get("id")).first()

        message = get_template('email/email_order_created.html').render({
            "base_info": GeneraliModel.get_solo(),
            "order":order
        })
 
        send_mail("Il tuo ordine è stato creato",message,from_email=EMAIL_HOST_USER,recipient_list=[self.request.user.email],html_message=message)

       
        return context_data'''


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

        message = get_template('email/email_order_paid.html').render({
            "base_info": GeneraliModel.get_solo(),
            "order":order
        }) 
        send_mail("Il tuo ordine è stato pagato",message,from_email=EMAIL_HOST_USER,recipient_list=[order.customer.email],html_message=message)

    return HttpResponse(status=200)