import imp
from catalogo.models import Category
from impostazioni.models import ImpostazioniGenerali



def base_info(request):
    return {
        "categories": Category.objects.all(),
        "base_info": ImpostazioniGenerali.get_solo(),
    }


