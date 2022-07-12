from django.views.generic import TemplateView, UpdateView


from django.urls import reverse_lazy, reverse
from django.contrib import messages

from .forms import AccountInformazioniEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User

from allauth.account.models import EmailConfirmation

class ProfiloView(LoginRequiredMixin, TemplateView):
    template_name = "account/index.html"
    redirect_field_name = 'redirect_to'

class AccountInformazioniProfiloView(TemplateView):
    template_name = "account/informazioni-profilo/view.html"

class AccountInformazioniProfiloEdit(UpdateView):
    model = User
    form_class = AccountInformazioniEditForm
    template_name = "account/informazioni-profilo/edit.html"

    def form_valid(self, form):
        messages.success(
            self.request, message="Informazioni aggiornate con successo!")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('le-mie-informazioni-edit', kwargs={'pk': self.object.id})



