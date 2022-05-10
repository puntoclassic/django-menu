from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.views import generic

from shopapp.forms import CustomLoginForm, CustomPasswordRecoveryForm, CustomSignInForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category

# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"

class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_url = "/account"

class CustomSignInView(generic.CreateView):
    template_name = "signin.html"
    form_class = CustomSignInForm
    success_url = reverse_lazy('login')

class CustomLogoutView(LogoutView):
    template_name = "logout.html"

class CustomPasswordRecoveryView(PasswordResetView):
    form_class = CustomPasswordRecoveryForm
    subject_template_name = "emails/recupera-password-subject.html"
    email_template_name = "emails/recupera-password-body.html"
    template_name = "recupera-password.html"

class CustomPasswordResetDone(TemplateView):
    template_name = "recupera-password-ok.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
        template_name = "recupera-password-conferma.html"

class CustomPasswordResetCompleted(TemplateView):
    template_name = "reset-password-completato.html"

class DashboardView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard.html"
    login_url = '/account/login'
    redirect_field_name = 'redirect_to'

class CategoriaListView(TemplateView):
    template_name = "categoria.html"
    children_categories = []

    def get(self, request, *args, **kwargs):      
        self.children_categories = Category.objects.filter(slug=kwargs["permalink"]).first().get_children()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["children_categories"] = self.children_categories
        return context_data
    