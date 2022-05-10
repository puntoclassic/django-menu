from django.urls import path, re_path
from shopapp.views import *

urlpatterns = [   
    path('',HomeView.as_view(),name='home'),
    path('account/login', CustomLoginView.as_view(), name='login'),
    path('account/signin',CustomSignInView.as_view(), name='signin'),
    path('account/logout',CustomLogoutView.as_view(), name='logout'),
    path('account/recupera-password',CustomPasswordRecoveryView.as_view(),name='recupera-password'),
    path('account/recupera-password/ok', CustomPasswordResetDone.as_view(),name='password_reset_done'),
    path('account/recupera-password/conferma/<uidb64>/<token>/',
       CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account',AccountView.as_view(), name='account'),
    path('account/reset-password/completato',CustomPasswordResetCompleted.as_view(),name='password_reset_complete'),
    re_path(r'^categorie/(?P<permalink>.*)$',CategoriaListView.as_view(),name='categoria'),
    path('account/form-contatto',AccountInviaMessaggio.as_view(),name='invia-messaggio'),
    path('account/form-contatto/ok',AccountInviaMessaggioDone.as_view(),name='invia-messaggio-ok')
]
