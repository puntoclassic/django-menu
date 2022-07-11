from commerce.models import Food
from profilo.models import User
from rest_framework import  serializers

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from allauth.account.models import EmailAddress 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from commerce.models import Category,Food

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
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()  

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        email = EmailAddress.objects.filter(email=user.email).first()
        token['emailVerified'] = email.verified   

        print(token);    

        return token

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        account = EmailAddress.objects.filter(email=user.email).first()

        # Add custom claims
        token['verified'] = account.verified
        # ...

        return token
