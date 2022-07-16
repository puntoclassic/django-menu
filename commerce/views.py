
from decimal import Decimal
from mimetypes import init
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


from commerce.forms import AddToCartForm, DecreaseQtyForm, IncreaseQtyForm, RemoveFromCartForm
from shop.settings import EMAIL_HOST_USER, env

from .models import Category, Food, Order, OrderDetail, OrderStatus, User, GeneraliModel
from .forms import AccountInformazioniEditForm, CheckoutConsegnaForm, CheckoutIndirizzoOrarioForm, CheckoutRiepilogoOrdineForm


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
                "tipo_consegna":"domicilio",
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
       
        initial["tipo_consegna"] = self.cart["tipo_consegna"] 
        return initial

    def form_valid(self, form):
        self.cart["tipo_consegna"] = form.cleaned_data["tipo_consegna"]        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:     
        self.request.session["cart"] = self.cart
        if self.cart["tipo_consegna"] == 'domicilio':            
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
    order = Order()
    
    def form_valid(self, form):
        cart = get_cart(self.request)
        note = form.cleaned_data["note"]        
        self.order.customer = self.request.user
        self.order.note = note
        self.order.shipping_address = cart["indirizzo"]
        self.order.shipping_delivery_time = cart["orario"]
        self.order.shipping_required = True if cart["tipo_consegna"] == "domicilio" else False
        self.order.shipping_costs = 2.00 if cart["tipo_consegna"] == "domicilio" else 0.00
        self.order.subtotal = Decimal(cart["amount"])+Decimal(self.order.shipping_costs)
        self.order.order_status = OrderStatus.objects.filter(description="Creato").first()
        self.order.save()  

        if self.order.shipping_required:
            order_row = OrderDetail()
            order_row.order = self.order
            order_row.name = "Spese di consegna"
            order_row.price = Decimal(self.order.shipping_costs)
            order_row.quantity = 1
            order_row.save()


        items = self.request.session["cart"]["items"] 
        for item in items.values():
            order_row = OrderDetail()
            order_row.order = self.order
            order_row.name = item["name"]
            order_row.price = Decimal(item["price"])
            order_row.quantity = item["quantity"]
            order_row.save()    



        del self.request.session["cart"]    

        message = get_template('email/email_order_created.html').render({
            "base_info": GeneraliModel.get_solo(),
            "order":self.order            
        })
 
        send_mail("Il tuo ordine è stato creato",message,from_email=EMAIL_HOST_USER,recipient_list=[self.request.user.email],html_message=message)   
 

        return super().form_valid(form)


    def get_success_url(self) -> str:
        messages.add_message(self.request,messages.SUCCESS,"Il tuo ordine è stato confermato","profilo-ordini")        
        return reverse('profilo-ordini-detail',kwargs={"pk":self.order.id})

    def test_func(self):
        return cart_not_empty(self)   

    def handle_no_permission(self) -> HttpResponseRedirect:
        return redirect(reverse_lazy('show-cart'))       

   

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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        messages.add_message(request,messages.SUCCESS,"Hai pagato il tuo ordine","profilo-ordini")
        return redirect(reverse('profilo-ordini-detail',kwargs={"pk":kwargs.get("id")}))


class GlobalSearchResultView(ListView):
    template_name: str = "global-search-result.html"
    queryset = Food.objects.all()
    model = Food

    def get_queryset(self) :
        search = self.request.GET.get("search","")
        queryset = super().get_queryset()
        if len(search)>0:
            queryset = queryset.filter(Q(name__icontains=search) | Q(ingredients__icontains=search) | Q(default_category__name__icontains=search))  
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["search"] = self.request.GET.get("search","")
        return context_data

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


class ProfiloView(LoginRequiredMixin, TemplateView):
    template_name = "account/index.html"
    redirect_field_name = 'redirect_to'

class AccountInformazioniProfiloView(TemplateView):
    template_name = "account/informazioni-profilo/view.html"

class AccountInformazioniProfiloEdit(UpdateView):
    model = User
    form_class = AccountInformazioniEditForm
    template_name = "account/informazioni-profilo/edit.html"

    def form_valid(self, form):
        messages.success(
            self.request, message="Informazioni aggiornate con successo!",extra_tags="informazioni-profilo")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('le-mie-informazioni-edit', kwargs={'pk': self.object.id})


class OrderListView(ListView):
    model = Order
    template_name = "account/order/order_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(customer=self.request.user)
        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = "account/order/order_detail.html"    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)