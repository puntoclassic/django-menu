from rest_framework import routers
from django.urls import path, include
from webapi.views import AccountActivateByCodeView, AccountResendActivationCodeView, AccountStatusView, RegisterView
from webapi.viewsets import CategoryViewSet, FoodViewSet 

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)

urlpatterns = [
    path('',include(router.urls)),  
    path('signin/', RegisterView.as_view(), name='auth_register'),
    path('login/getToken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refreshToken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verifyToken/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/verifyAccount/', AccountActivateByCodeView.as_view(), name='verify_account_by_code'),
    path('login/accountStatus/', AccountStatusView.as_view(), name='account_status_api'),
    path('login/resendActivationCode/', AccountResendActivationCodeView.as_view(), name='resend_activation_code'),
]