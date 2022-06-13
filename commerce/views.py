
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView


from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category

# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"   

    def get(self, request, *args, **kwargs):

        first_category = Category.objects.first()

        if first_category is not None:
            return redirect('category-show',slug=first_category.slug)  
        else:
            return redirect('error-page')    
        return super().get(request, *args, **kwargs) 

class ErrorPageView(TemplateView):
    template_name = "error.html"  



class CategoriaListView(DetailView):
    template_name = "categoria.html"
    model = Category
   

    def get_object(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.model.objects.filter(slug=self.kwargs['slug']).first()

    '''def get(self, request, *args, **kwargs):      
        category = get_object_or_404(Category, slug=self.kwargs['permalink'])
        if category:
            self.children_categories = Category.objects.filter(slug=kwargs["permalink"]).first().get_children()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["children_categories"] = self.children_categories
        context_data["anchestors_categories"] = self.anchestors_categories
        return context_data'''

#profile views
