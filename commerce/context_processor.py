import imp
from .models import Category



def base_categories(request):
    return {
        "categories": Category.objects.all()
    }
