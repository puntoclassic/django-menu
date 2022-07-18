from django.contrib import admin

from .models import Order, OrderDetail, OrderStatus

@admin.register(OrderStatus)
class AdminOrderStatus(admin.ModelAdmin):
    list_display = ('description',)

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id','customer_name','subtotal',)

    def customer_name(self,obj:Order): 
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    customer_name.short_description = "Cliente"



