import graphene
from graphene_django import DjangoObjectType

from commerce.models import Category, Food


class CategoryType(DjangoObjectType):
    image_url = graphene.String(source='image_url')
    class Meta:
        model = Category
        fields = ("id", "name", "image","image_url")

class FoodType(DjangoObjectType):
    class Meta:
        model = Food
        fields = ("id", "name", "ingredients","price")

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    foods = graphene.List(FoodType)
    foodsByCategory = graphene.List(FoodType, categoryId=graphene.Int(required=True))

    def resolve_categories(root, info):
        return Category.objects.all()
    
    def resolve_foods(root, info):
        return Food.objects.all()

    def resolve_foodsByCategory(root, info,categoryId):
        return Food.objects.filter(default_category__id=categoryId).all()

schema = graphene.Schema(query=Query)