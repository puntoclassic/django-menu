from django.urls import path

from commerce.models import Food
from .views import *
from rest_framework import routers, serializers, viewsets
from django.urls import path, include


# Serializers define the API representation.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image']

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food        
        fields = ['id','name','ingredients','default_category','price']

# ViewSets define the view behavior.
class FoodViewSet(viewsets.ModelViewSet):     
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('api/',include(router.urls)),
    path('', HomeView.as_view(), name='home'),
    path('categoria/<slug:slug>', CategoriaListView.as_view(), name='category-show'),
    path('errore', ErrorPageView.as_view(), name='error-page'),
    path('carrello', CartView.as_view(), name='show-cart'),
    path('carrello/aggiungiAlCarrello',
         AddToCartView.as_view(), name='add-to-cart'),
    path('carrello/rimuoviDalCarrello',
         RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('carrello/incrementaQuantità',
         IncreaseQtyView.as_view(), name='increase-qty'),
    path('carrello/riduciQuantità',
         DecreaseQtyView.as_view(), name='decrease-qty'),
     path('checkout/consegna', CheckoutConsegnaView.as_view() ,name="checkout-consegna"),
     path('checkout/consegna/dettagli', CheckoutIndirizzoOrarioView.as_view() ,name="checkout-indirizzo-orario"),
     path('checkout/riepilogo', CheckoutRiepilogoView.as_view() ,name="checkout-riepilogo"),
     path('checkout/ordine/<int:id>/confermato', CheckoutConfermaView.as_view() ,name="checkout-conferma")
]
