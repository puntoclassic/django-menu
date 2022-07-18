from catalogo.models import Food, Category
from rest_framework import  serializers
from impostazioni.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from allauth.account.models import EmailAddress

import random
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','image']


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food        
        fields = ['id','name','ingredients','default_category','price']

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
        activation_code = str(random.randrange(100000,999999))

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            activation_code=activation_code,
            email_verified=False
        )
        
        user.set_password(validated_data['password'])
        user.save()        

        return user

class AccountActivationByCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)      

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        emailAddress = EmailAddress.objects.filter(email=user.email).first()

        token['verified'] = emailAddress.verified
        return token
