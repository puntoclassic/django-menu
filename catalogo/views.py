
from django.views.generic import DetailView
from django.views.generic.list import ListView
from .models import Category, Food
from django.db.models import Q

class CategoriaListView(DetailView):
    template_name = "catalogo/categoria.html"
    model = Category

    def get_object(self):
        return self.model.objects.filter(slug=self.kwargs['slug']).first()


class GlobalSearchResultView(ListView):
    template_name: str = "catalogo/global-search-result.html"
    queryset = Food.objects.all()
    model = Food

    def get_queryset(self) :
        search = self.request.GET.get("search","")
        queryset = super().get_queryset()
        if len(search)>0:
            queryset = queryset.filter(Q(name__icontains=search) | Q(ingredients__icontains=search) | Q(default_category__name__icontains=search))  
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["search"] = self.request.GET.get("search","")
        return context_data


