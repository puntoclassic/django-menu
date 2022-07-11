from django.contrib import admin
from django.urls import include, path, include

from commerce.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('commerce.urls')),
    path('auth/', include('profilo.urls')),
    path('auth/', include('allauth.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/', include('webapi.urls')),
    
]
