
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy, reverse
from django.views import generic

from commerce.forms import ContactForm, CustomLoginForm, CustomPasswordRecoveryForm, CustomSignInForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category

# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"    

class CustomLoginView(LoginView):
    template_name = "login.html"
    form_class = CustomLoginForm
    redirect_url = reverse_lazy('account')

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

class AccountView(LoginRequiredMixin,TemplateView):
    template_name = "account/index.html"
    redirect_field_name = 'redirect_to'

class CategoriaListView(DetailView):
    template_name = "categoria.html"
    model = Category
    children_categories = []
    anchestors_categories = []

    def get_object(self):
        category = get_object_or_404(Category, slug=self.kwargs['permalink'])
        self.anchestors_categories = category.get_ancestors(include_self=True)
        return self.model.objects.filter(slug=self.kwargs['permalink']).first()

    def get(self, request, *args, **kwargs):      
        category = get_object_or_404(Category, slug=self.kwargs['permalink'])
        if category:
            self.children_categories = Category.objects.filter(slug=kwargs["permalink"]).first().get_children()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["children_categories"] = self.children_categories
        context_data["anchestors_categories"] = self.anchestors_categories
        return context_data

    
class AccountInviaMessaggio(LoginRequiredMixin,FormView):
    template_name = 'account/form-contatto.html'
    form_class = ContactForm
    success_url = reverse_lazy('invia-messaggio-ok')

    def get(self, request, *args, **kwargs):
        self.initial["first_name"] = request.user.first_name
        self.initial["last_name"] = request.user.last_name
        self.initial["email"] = request.user.email

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):      
        return super().form_valid(form)

class AccountInviaMessaggioDone(LoginRequiredMixin,TemplateView):
    template_name = 'account/form-contatto-ok.html'