from django.urls import path


from .views import *
from django.urls import path, include




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
    path('checkout/consegna', CheckoutConsegnaView.as_view() ,name="checkout-consegna"),
    path('checkout/consegna/dettagli', CheckoutIndirizzoOrarioView.as_view() ,name="checkout-indirizzo-orario"),
    path('checkout/riepilogo', CheckoutRiepilogoView.as_view() ,name="checkout-riepilogo"),    
    path('webhook/', stripe_webhook), 
    path('cerca',GlobalSearchResultView.as_view(),name='search'),
    path('account/', ProfiloView.as_view(), name='profilo'),   
    path('account/informazioni/', AccountInformazioniProfiloView.as_view(),
         name='le-mie-informazioni-view'),
    path('account/informazioni/edit/<int:pk>',
         AccountInformazioniProfiloEdit.as_view(), name='le-mie-informazioni-edit'),  
    path('account/ordini/list',OrderListView.as_view(),name='profilo-ordini-list'),
    path('account/ordini/detail/<int:pk>',OrderDetailView.as_view(),name='profilo-ordini-detail'),
    path('account/ordini/pagamento/<int:id>', CheckoutPagaView.as_view() ,name="checkout-paga"),
    path('account/ordini/pagamento/completato/<int:id>', CheckoutPagatoView.as_view() ,name="checkout-pagato"),   
]
