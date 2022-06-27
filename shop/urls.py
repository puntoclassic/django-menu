from django.contrib import admin
from django.urls import include, path, include
from django.contrib.auth import views as auth_views

from commerce.views import *

from rest_framework import routers, serializers, viewsets


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('commerce.urls')),
    path('auth/', include('profilo.urls')),
    path('auth/', include('allauth.urls')),
    path('api/', include('rest_framework.urls')),
]
