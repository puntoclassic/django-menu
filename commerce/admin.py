from django.contrib import admin
from commerce.actions import categories_update_slug

from commerce.models import Category, Food, Order, OrderStatus

# Register your models here.


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    actions = (categories_update_slug,)


@admin.register(Food)
class AdminFood(admin.ModelAdmin):
    list_display = ('name', 'price', 'ingredients', 'default_category',)


@admin.register(OrderStatus)
class AdminOrderStatus(admin.ModelAdmin):
    list_display = ('description',)

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id','customer_name','subTotal',)

    def customer_name(self,obj:Order): 
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    customer_name.short_description = "Cliente"