from commerce.models import Food
from profilo.models import User
from rest_framework import routers, serializers, viewsets
from django.urls import path, include
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import generics
from rest_framework.permissions import AllowAny
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from commerce.models import Category,Food
from rest_framework import mixins
from rest_framework.views import APIView

# Serializers define the API representation.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image']

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food        
        fields = ['id','name','ingredients','default_category','price']

# ViewSets define the view behavior.
class FoodViewSet(viewsets.ModelViewSet):     
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()  

        return user
    
   
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


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):       
        return Response({
            "nome":request.user.first_name,
            "cognome":request.user.last_name
        })   
   


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'foods', FoodViewSet)




urlpatterns = [
    path('',include(router.urls)),  
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user/',UserView.as_view())
]
