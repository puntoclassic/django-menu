from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Categoria/<slug:slug>', CategoriaListView.as_view(), name='category-show'),
    path('Errore', ErrorPageView.as_view(), name='error-page'),
    path('Carrello', CartView.as_view(), name='show-cart'),
    path('Carrello/AggiungiAlCarrello',
         AddToCartView.as_view(), name='add-to-cart'),
    path('Carrello/RimuoviDalCarrello',
         RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('Carrello/IncrementaQuantità',
         IncreaseQtyView.as_view(), name='increase-qty'),
    path('Carrello/RiduciQuantità',
         DecreaseQtyView.as_view(), name='decrease-qty'),
]
