import imp
from .models import GeneraliModel


def base_info(request):
    return {
        "base_info": GeneraliModel.get_solo()
    }
