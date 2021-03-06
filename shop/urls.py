from django.contrib import admin
from django.urls import include, path, include

from commerce.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('commerce.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/', include('webapi.urls')),
    path('',include('impostazioni.urls')),
    path('',include('catalogo.urls')),
    path('',include('vendite.urls'))
]
