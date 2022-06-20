from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('Categoria/<slug:slug>', CategoriaListView.as_view(), name='category-show'),
    path('errore', ErrorPageView.as_view(), name='error-page'),

]
