from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [       
    path('', ProfiloView.as_view(), name='profilo'),   
    path('le-mie-informazioni/', AccountInformazioniProfiloView.as_view(),
         name='le-mie-informazioni-view'),
    path('le-mie-informazioni/edit/<int:pk>',
         AccountInformazioniProfiloEdit.as_view(), name='le-mie-informazioni-edit'),   
]
