
from rest_framework import routers
from django.urls import path, include
from webapi.views import RegisterView, UserView
from webapi.viewsets import CategoryViewSet, FoodViewSet 
   


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('',include(router.urls)),  
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/',UserView.as_view())
]
