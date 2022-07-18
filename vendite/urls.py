from django.urls import path


from .views import *
from django.urls import path, include




urlpatterns = [   
    path('carrello', CartView.as_view(), name='vendite.carrello'),
    path('carrello/aggiungiAlCarrello',
         AddToCartView.as_view(), name='vendite.carrello.aggiungi'),
    path('carrello/rimuoviDalCarrello',
         RemoveFromCartView.as_view(), name='vendite.carrello.rimuovi'),
    path('carrello/incrementaQuantità',
         IncreaseQtyView.as_view(), name='vendite.carrello.aumentaQta'),
    path('carrello/riduciQuantità',
         DecreaseQtyView.as_view(), name='vendite.carrello.riduciQta'),
    path('cassa/consegna', CassaConsegnaView.as_view() ,name="vendite.cassa.consegna"),
    path('cassa/consegna/dettagli', CassaIndirizzoOrarioView.as_view() ,name="vendite.cassa.indirizzo.orario"),
    path('cassa/riepilogo', CassaRiepilogoView.as_view() ,name="vendite.cassa.riepilogo"),    
    path('webhook/', stripe_webhook), 
    path('account/ordini/elenco',OrderListView.as_view(),name='vendite.ordine.list'),
    path('account/ordini/dettaglio/<int:pk>',OrderDetailView.as_view(),name='vendite.ordine.detail'),
    path('account/ordini/pagamento/<int:id>', CassaPagaView.as_view() ,name="vendite.ordine.paga"),
    path('account/ordini/pagamento/completato/<int:id>', CassaPagatoView.as_view() ,name="vendite.ordine.pagato"),   
]
