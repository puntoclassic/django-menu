from django.urls import path
from webapi.views import AccountActivateByCodeView, AccountResendActivationCodeView, MyTokenObtainPairView, RegisterView

from rest_framework import routers
from django.urls import path, include
from commerce.models import Category, Food
from webapi.schema import CategoryApiResponse, FoodApiResponse, MyTokenObtainPairOutSchema, MyTokenObtainPairSchema
from webapi.views import AccountActivateByCodeView, AccountResendActivationCodeView, MyTokenObtainPairView, RegisterView
from ninja_extra import api_controller, route
from ninja_jwt.controller import TokenObtainPairController, TokenVerificationController
from typing import List
from ninja_extra import NinjaExtraAPI
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)





api = NinjaExtraAPI()

@api_controller('login', tags=['Auth'])
class MyObtainTokenController(TokenObtainPairController):
    @route.post(
        "/pair", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair"
    )
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        return user_token.output_schema()

@api_controller('login', tags=['Auth'])
class MyVerifyTokenController(TokenVerificationController):
    pass

api.register_controllers(MyObtainTokenController)
api.register_controllers(MyVerifyTokenController)


@api.get("/categories",response=List[CategoryApiResponse])
def categories(request):
    return Category.objects.all()

@api.get("/foods",response=List[FoodApiResponse])
def foods(request):
    return Food.objects.all()

@api.get("/foods/byCategory/{category_id}",response=List[FoodApiResponse])
def foodsByCategory(request,category_id: int):
    return Food.objects.filter(default_category__id=category_id)


urlpatterns = [   
    path('',api.urls),  
    path('signin/', RegisterView.as_view(), name='auth_register'), 
    path('login/verifyAccount/', AccountActivateByCodeView.as_view(), name='verify_account_by_code'),
    path('login/resendActivationCode/', AccountResendActivationCodeView.as_view(), name='resend_activation_code'),
]