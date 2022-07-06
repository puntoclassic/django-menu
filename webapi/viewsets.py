from commerce.models import Food
from profilo.models import User
from rest_framework import serializers, viewsets

from rest_framework.response import Response
from commerce.models import Category,Food

from rest_framework.decorators import action




class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','first_name','last_name']
