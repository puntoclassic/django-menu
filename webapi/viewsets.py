from catalogo.models import Food,Category
from rest_framework import serializers, viewsets

from rest_framework.response import Response
from impostazioni.models import User

from rest_framework.decorators import action

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id','first_name','last_name']

from webapi.serializers import CategorySerializer, FoodSerializer


# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'], name='Get By Category',url_path=r"foods", url_name='Get food by category',)
    def get_by_category(self, request, pk=None):
        obj = self.get_object().foods.all()

        serializer = FoodSerializer(obj, many=True)
        return Response(serializer.data)


# ViewSets define the view behavior.
class FoodViewSet(viewsets.ModelViewSet):     
    queryset = Food.objects.all()
    serializer_class = FoodSerializer  
