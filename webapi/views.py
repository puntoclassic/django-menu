
import email
from profilo.models import User

from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.template.loader import get_template

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from shop.settings import EMAIL_HOST_USER
from allauth.account.models import EmailAddress
from impostazioni.models import GeneraliModel

from webapi.serializers import AccountActivationByCodeSerializer, MyTokenObtainPairSerializer, RegisterSerializer
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer  

    def create(self, request, *args, **kwargs):
        email = str(request.data["email"]).lower()

        if(User.objects.filter(email=email).first() is not None):
            return Response(
            {
                "status":"Email is busy"              
            }
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()      


        message = get_template('email/email_activation_code.html').render({
            "base_info": GeneraliModel.get_solo(),
            "code":user.activation_code
        }) 
        send_mail("Attiva il tuo account",message,from_email=EMAIL_HOST_USER,recipient_list=[user.email],html_message=message)
     
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
            "status":"Account activated"
        })
        else:        
            return Response({
                "status":"Verifica fallita"
            })


class AccountResendActivationCodeView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def post(self, request, *args, **kwargs):
        message = get_template('email/email_activation_code.html').render({
            "base_info": GeneraliModel.get_solo(),
            "code":request.user.activation_code
        }) 
        send_mail("Attiva il tuo account",message,from_email=EMAIL_HOST_USER,recipient_list=[request.user.email],html_message=message)

        return Response({})



           

        

       


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
