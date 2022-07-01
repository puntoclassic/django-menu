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
from rest_framework.decorators import action

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
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()  

        return user