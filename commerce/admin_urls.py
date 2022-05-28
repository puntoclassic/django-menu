from django.urls import path, re_path
from commerce.admin_views import AdminCategoryUpdateView, AdminCategoryListView, AdminHome


urlpatterns = [   
    path('',AdminHome.as_view(),name='amministrazione'),
    path('categorie',AdminCategoryListView.as_view(),name='admin_category_listview'),  
    path('categorie/edit/<int:pk>',AdminCategoryUpdateView.as_view(),name='admin_category_updateview')   
]