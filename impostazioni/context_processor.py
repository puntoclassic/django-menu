import imp
from .models import Category, GeneraliModel



def base_info(request):
    return {
        "base_info":GeneraliModel.objects.get()
    }