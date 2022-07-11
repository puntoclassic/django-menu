from rest_framework import routers
from django.urls import path, include
from webapi.views import LoginView, MyTokenObtainPairView, RegisterView, UserView
from webapi.viewsets import CategoryViewSet, FoodViewSet 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('',include(router.urls)),  
    path('user/',UserView.as_view()),
    path('user/login/',LoginView.as_view()),
    path('user/signin/', RegisterView.as_view(), name='auth_register'),
    path('user/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]