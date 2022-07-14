import imp
from .models import Category, GeneraliModel



def base_info(request):
    return {
        "categories": Category.objects.all(),
        "base_info": GeneraliModel.get_solo(),
    }


