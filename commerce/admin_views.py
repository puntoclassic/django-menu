from email import message
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Category
from django.contrib import messages
from django.db.models import Q


class AdminHome(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    template_name = "admin/home.html"

    def test_func(self):
        return self.request.user.is_staff

#categorie
class AdminCategoryListView(ListView):
    model = Category
    template_name = "admin/admin_category_listview.html"
    paginate_by = 25

    def get(self, request, *args, **kwargs):
        print(self.request.GET.get("search_key")=="")
        if self.request.GET.get("search_key") is not None and self.request.GET.get("search_key")=="":
            print("SOno qui dentro")
            return redirect('admin_category_listview')
        return super().get(request, *args, **kwargs)


    def get_queryset(self):

        if self.request.GET.get("by_parent"):
            return super().get_queryset().filter(parent_id=self.request.GET.get("by_parent"))
        
        if self.request.GET.get("search_key"):
            chiave = self.request.GET.get("search_key")
            return super().get_queryset().filter(name__icontains=chiave)
        
        queryset = super().get_queryset().filter(level=0)
        return queryset

class AdminCategoryUpdateView(UpdateView):
    model = Category
    template_name = "admin/admin_category_updateview.html"
    fields = ('name','active','parent',)
  

    def get_success_url(self) -> str:
        messages.add_message(self.request,messages.SUCCESS,"Categoria aggiornata")
        return reverse('admin_category_updateview',kwargs={"pk":self.object.id})

