from rest_framework import routers
from django.urls import path, include
from webapi.views import MyTokenObtainPairView, RegisterView
from webapi.viewsets import CategoryViewSet, FoodViewSet 

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('',include(router.urls)),  
    path('user/signin/', RegisterView.as_view(), name='auth_register'),
    path('user/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/verify/', TokenVerifyView.as_view(), name='token_verify'),

]