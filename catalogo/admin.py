from django.contrib import admin
from .actions import categories_update_slug

from .models import Category, Food

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    actions = (categories_update_slug,)


@admin.register(Food)
class AdminFood(admin.ModelAdmin):
    list_display = ('name', 'price', 'ingredients', 'default_category',)
