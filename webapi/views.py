
from profilo.models import User

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView

from webapi.serializers import MyTokenObtainPairSerializer, RegisterSerializer
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
        
        #TODO: send activation code
        headers = self.get_success_headers(serializer.data)

        return Response(
            {
                "status":"User created"              
            }
        , status=status.HTTP_201_CREATED, headers=headers)   


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
