from django.urls import path
from .views import *

urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('signin', CustomSignInView.as_view(), name='signin'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('recupera-password', CustomPasswordResetView.as_view(),
         name='recupera-password'),
    path('recupera-password/done', CustomPasswordResetDone.as_view(),
         name='password_reset_done'),
    path('recupera-password/conferma/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', ProfiloView.as_view(), name='profilo'),
    path('reset-password/completato', CustomPasswordResetCompleted.as_view(),
         name='password_reset_complete'),
    path('form-contatto', AccountInviaMessaggio.as_view(), name='invia-messaggio'),
    path('form-contatto/completato',
         AccountInviaMessaggioDone.as_view(), name='invia-messaggio-ok'),
    path('le-mie-informazioni/', AccountInformazioniProfiloView.as_view(),
         name='le-mie-informazioni-view'),
    path('le-mie-informazioni/edit/<int:pk>',
         AccountInformazioniProfiloEdit.as_view(), name='le-mie-informazioni-edit'),
    path('cambia-password', AccountCambiaPassword.as_view(), name='cambia-password'),
    path('cambia-password/completato',
         AccountCambiaPasswordDone.as_view(), name='cambia-password-done'),


]
