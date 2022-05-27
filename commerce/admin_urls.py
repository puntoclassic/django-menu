from django.urls import path, re_path
from commerce.admin_views import *

urlpatterns = [   
    path('',AdminHome.as_view(),name='amministrazione')   

]