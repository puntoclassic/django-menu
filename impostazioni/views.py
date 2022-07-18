from django.urls import reverse
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import User
from .forms import AccountInformazioniEditForm

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
            self.request, message="Informazioni aggiornate con successo!",extra_tags="informazioni-profilo")
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('impostazioni.profilo.informazioni.edit', kwargs={'pk': self.object.id})
