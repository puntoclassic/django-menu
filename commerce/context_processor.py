import imp
from .models import Category
import feedparser


def base_categories(request):
    return {
        "base_categories": Category.objects.filter(level=0)
    }
