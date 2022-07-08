from rest_framework import routers
from django.urls import path, include
from webapi.views import LoginView, RegisterView, UserView
from django.views.decorators.csrf import csrf_exempt
from webapi.viewsets import CategoryViewSet, FoodViewSet 



# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('',include(router.urls)),  
    path('user/',UserView.as_view()),
    path('user/login/',LoginView.as_view()),
    path('user/signin/', RegisterView.as_view(), name='auth_register'),
]