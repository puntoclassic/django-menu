import imp
from catalogo.models import Category
from impostazioni.models import GeneraliModel



def base_info(request):
    return {
        "categories": Category.objects.all(),
        "base_info": GeneraliModel.get_solo(),
    }


