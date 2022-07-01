
from profilo.models import User

from rest_framework import generics
from rest_framework.permissions import AllowAny
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from webapi.serializers import RegisterSerializer
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()
        complete_signup(self.request._request, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return user


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):       
        return Response({
            "nome":request.user.first_name,
            "cognome":request.user.last_name
        })   