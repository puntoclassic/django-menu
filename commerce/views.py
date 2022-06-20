
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView


from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category

# Create your views here.


class HomeView(TemplateView):
    template_name = "index.html"


class ErrorPageView(TemplateView):
    template_name = "error.html"


class CategoriaListView(DetailView):
    template_name = "categoria.html"
    model = Category

    def get_object(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.model.objects.filter(slug=self.kwargs['slug']).first()

# profile views
