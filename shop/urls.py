from django.contrib import admin
from django.urls import include, path, include
from django.contrib.auth import views as auth_views

from commerce.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('commerce.urls'))
]
