from django.urls import path


from .views import *
from django.urls import path, include


urlpatterns = [    
    path('account/', include('allauth.urls')),
    path('account/', ProfiloView.as_view(), name='impostazioni.profilo.index'),   
    path('account/informazioni/', AccountInformazioniProfiloView.as_view(),
         name='impostazioni.profilo.informazioni.view'),
    path('account/informazioni/edit/<int:pk>',
         AccountInformazioniProfiloEdit.as_view(), name='impostazioni.profilo.informazioni.edit'),     
]
