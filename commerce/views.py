
from django.views.generic import TemplateView


# Create your views here.

class HomeView(TemplateView):
    template_name = "commerce/index.html"


class ErrorPageView(TemplateView):
    template_name = "commerce/error.html"

