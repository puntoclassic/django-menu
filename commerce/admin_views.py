from email import message
from django.urls import reverse
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Category
from django.contrib import messages


class AdminHome(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    template_name = "admin/home.html"

    def test_func(self):
        return self.request.user.is_staff

#categorie
class AdminCategoryListView(ListView):
    model = Category
    template_name = "admin/admin_category_listview.html"
    paginate_by = 25

    def get_queryset(self):

        if self.request.GET.get("by_parent"):
            return super().get_queryset().filter(parent_id=self.request.GET.get("by_parent"))
        
        queryset = super().get_queryset().filter(level=0)
        return queryset

class AdminCategoryUpdateView(UpdateView):
    model = Category
    template_name = "admin/admin_category_updateview.html"
    fields = ('name','active','parent',)
  

    def get_success_url(self) -> str:
        messages.add_message(self.request,messages.SUCCESS,"Categoria aggiornata")
        return reverse('admin_category_updateview',kwargs={"pk":self.object.id})

