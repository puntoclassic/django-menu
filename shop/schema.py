import graphene
from graphene_django import DjangoObjectType
from pkg_resources import require
from django.contrib.auth import authenticate
from allauth.account.models import EmailAddress 

from commerce.models import Category, Food
from graphene import Dynamic, JSONString, relay, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from graphene.types.generic import GenericScalar

from profilo.models import User


class CategoryType(DjangoObjectType):
    image_url = graphene.String(source='image_url')
    class Meta:
        model = Category
        fields = ("id", "name", "image","image_url","foods")

class FoodType(DjangoObjectType):
    pk = graphene.Int(source='pk')
    class Meta:
        model = Food
        fields = ("id", "name", "ingredients","price")
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'ingredients': ['exact', 'icontains', 'istartswith'],            
        }
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    foods = DjangoFilterConnectionField(FoodType)
    foodsByCategory = graphene.List(FoodType, categoryId=graphene.Int(required=True))
    login = graphene.Field(GenericScalar,email=graphene.String(required=True),password=graphene.String(required=True))

    def resolve_categories(root, info):
        return Category.objects.all()  

    def resolve_foodsByCategory(root, info,categoryId):
        return Food.objects.filter(default_category__id=categoryId).all()        

    def resolve_login(root,info,email,password):
        email = str(email).lower()
        user = authenticate(username=email,password=password)

        if user is not None:
            account = EmailAddress.objects.filter(email=email).first()
            return {
                "status":"Ok",
                "user_id":user.id,
                "verified":account.verified
            }
        else:
            return {
                "status":"Login failed"              
            }

class SigninMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        email = graphene.String(required=True)
        firstname = graphene.String(required=True)
        lastname = graphene.String(required=True)
        password = graphene.String(required=True)        

    # The class attributes define the response of the mutation
    response = graphene.Field(GenericScalar)

    @classmethod
    def mutate(cls, root, info, firstname,lastname,email,password):
        emailTest = EmailAddress.objects.filter(email=email).first()
        if emailTest is not None:
            return SigninMutation(response={
            "status":"Email is busy"            
            })
        user = User.objects.create(first_name=firstname,last_name=lastname,username=email,email=email)
        user.set_password(password)
        user.save()
        complete_signup(info.context, user,
                        allauth_settings.EMAIL_VERIFICATION,
                        None)
        return SigninMutation(response={
            "status":"User created"            
        })
        # Notice we return an instance of this mutation
        return 

class Mutation(graphene.ObjectType):
    signin = SigninMutation.Field()
        

schema = graphene.Schema(query=Query,mutation=Mutation)