from django.contrib import admin
from commerce.actions import categories_update_slug

from commerce.models import Category, Food

# Register your models here.


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    actions = (categories_update_slug,)


@admin.register(Food)
class AdminFood(admin.ModelAdmin):
    list_display = ('name', 'price', 'ingredients', 'default_category',)
