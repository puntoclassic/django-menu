
from rest_framework import routers
from django.urls import path, include
from webapi.views import LoginView, RegisterView, UserView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),  
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/',UserView.as_view()),
    path('user/login/',LoginView.as_view()),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
