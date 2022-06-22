from django.views.generic import TemplateView, UpdateView, CreateView
from django.contrib.auth.views import PasswordResetConfirmView,  PasswordChangeDoneView, LogoutView,  PasswordResetView, PasswordChangeView, PasswordResetDoneView

from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages

from .forms import AccountInformazioniEditForm, ContactForm, CustomLoginForm, CustomPasswordRecoveryForm, CustomSignInForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from allauth.account.views import LoginView
from .models import User
# Create your views here.


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    redirect_url = reverse_lazy('account')


class CustomSignInView(CreateView):
    template_name = "profilo/signin.html"
    form_class = CustomSignInForm
    success_url = reverse_lazy('login') 
 


class CustomLogoutView(LogoutView):
    template_name = "profilo/logout.html"


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordRecoveryForm
    subject_template_name = "account/email/recupera-password-subject.html"
    email_template_name = "account/email/recupera-password-body.html"
    html_email_template_name = "account/email/recupera-password-body.html"
    template_name = "profilo/recupera-password/recupera-password-1.html"


class CustomPasswordResetDone(PasswordResetDoneView):
    template_name = "profilo/recupera-password/recupera-password-2.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "profilo/recupera-password/recupera-password-3.html"


class CustomPasswordResetCompleted(PasswordChangeDoneView):
    template_name = "profilo/recupera-password/recupera-password-4.html"


class ProfiloView(LoginRequiredMixin, TemplateView):
    template_name = "profilo/index.html"
    redirect_field_name = 'redirect_to'


class AccountInviaMessaggio(LoginRequiredMixin, FormView):
    template_name = 'form-contatto/form-contatto-1.html'
    form_class = ContactForm
    success_url = reverse_lazy('invia-messaggio-ok')

    def get(self, request, *args, **kwargs):
        self.initial["first_name"] = request.user.first_name
        self.initial["last_name"] = request.user.last_name
        self.initial["email"] = request.user.email

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class AccountInviaMessaggioDone(LoginRequiredMixin, TemplateView):
    template_name = 'form-contatto/form-contatto-2.html'


class AccountInformazioniProfiloView(TemplateView):
    template_name = "profilo/informazioni-profilo/view.html"


class AccountInformazioniProfiloEdit(UpdateView):
    model = User
    form_class = AccountInformazioniEditForm
    template_name = "profilo/informazioni-profilo/edit.html"

    def form_valid(self, form):
        messages.success(
            self.request, message="Informazioni aggiornate con successo!")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('le-mie-informazioni-edit', kwargs={'pk': self.object.id})


class AccountCambiaPassword(PasswordChangeView):
    template_name = "profilo/cambia-password/cambia-password-1.html"
    success_url = reverse_lazy("cambia-password-done")


class AccountCambiaPasswordDone(TemplateView):
    template_name = "profilo/cambia-password/cambia-password-2.html"
