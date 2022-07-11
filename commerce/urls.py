from django.urls import path
from .views import *
from django.urls import path, include

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
   
]
