import graphene
from graphene_django import DjangoObjectType


from commerce.models import Category, Food
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField



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

    def resolve_categories(root, info):
        return Category.objects.all()  

    def resolve_foodsByCategory(root, info,categoryId):
        return Food.objects.filter(default_category__id=categoryId).all()        
   
        

schema = graphene.Schema(query=Query)