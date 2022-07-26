

import random
import django
from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenObtainSlidingView
from django.core.mail import send_mail
from django.template.loader import get_template

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from impostazioni.forms import CustomSignInForm
from shop.settings import EMAIL_HOST_USER
from allauth.account.models import EmailAddress
from impostazioni.models import ImpostazioniGenerali, User
from django.views.decorators.csrf import csrf_protect 

from webapi.serializers import AccountActivationByCodeSerializer, RegisterSerializer
# Create your views here.
from django.utils.decorators import method_decorator

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer     

    @ method_decorator(csrf_protect)
    def create(self, request, *args, **kwargs):  
       
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()    
        activation_code = str(random.randrange(100000,999999))

        user.activation_code = activation_code
        user.save()

        message = get_template('account/email/email_activation_code.html').render({
            "base_info": ImpostazioniGenerali.get_solo(),
            "code":request.user.activation_code
        }) 
        send_mail("Attiva il tuo account",message,from_email=EMAIL_HOST_USER,recipient_list=[request.user.email],html_message=message)       
     
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status":"User created"              
            }
        , status=status.HTTP_201_CREATED, headers=headers)   


class AccountActivateByCodeView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountActivationByCodeSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   

        if str(request.data["code"])==request.user.activation_code:
            emailAddress = EmailAddress.objects.filter(email=request.user.email).first()
            emailAddress.verified = True
            emailAddress.save()
            return Response({
            "status":"Ok"
        })
        else:        
            return Response({
                "status":"Verifica fallita"
            })


class AccountResendActivationCodeView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):

        activation_code = str(random.randrange(100000,999999))

        request.user.activation_code = activation_code
        request.user.save()

        message = get_template('account/email/email_activation_code.html').render({
            "base_info": ImpostazioniGenerali.get_solo(),
            "code":request.user.activation_code
        }) 
        send_mail("Attiva il tuo account",message,from_email=EMAIL_HOST_USER,recipient_list=[request.user.email],html_message=message)

        return Response({})      


class AccountStatusView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):

        return Response({
            "verified":request.user.verified
        })



    


    