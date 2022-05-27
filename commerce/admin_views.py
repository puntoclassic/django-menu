from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class AdminHome(LoginRequiredMixin,UserPassesTestMixin, TemplateView):
    template_name = "admin/home.html"

    def test_func(self):
        return self.request.user.is_staff