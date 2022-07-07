from django.contrib import admin
from django.urls import include, path, include
from django.contrib.auth import views as auth_views
from graphene_django.views import GraphQLView

from commerce.views import *

from rest_framework import routers, serializers, viewsets
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('commerce.urls')),
    path('auth/', include('profilo.urls')),
    path('auth/', include('allauth.urls')),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
