from django.urls import path


from .views import *
from django.urls import path, include




urlpatterns = [
    path('cerca',GlobalSearchResultView.as_view(),name='catalogo.cerca'),
    path('categoria/<slug:slug>', CategoriaListView.as_view(), name='catalogo.categoria.show'),   
]
