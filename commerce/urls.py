from django.urls import path
from .views import *

urlpatterns = [
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
]
