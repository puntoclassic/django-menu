from django.urls import path
from .views import *
'''
path('login', CustomLoginView.as_view(), name='login'),

path('cambia-password', AccountCambiaPassword.as_view(), name='cambia-password'),
path('cambia-password/completato',AccountCambiaPasswordDone.as_view(), name='cambia-password-done'),

'''

urlpatterns = [   
   
    path('', ProfiloView.as_view(), name='profilo'),
   
    path('le-mie-informazioni/', AccountInformazioniProfiloView.as_view(),
         name='le-mie-informazioni-view'),
    path('le-mie-informazioni/edit/<int:pk>',
         AccountInformazioniProfiloEdit.as_view(), name='le-mie-informazioni-edit'),
    

]
