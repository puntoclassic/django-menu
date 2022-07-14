from django.contrib import admin
from commerce.actions import categories_update_slug

from commerce.models import Category, Food, GeneraliModel, Order, OrderDetail, OrderStatus, User
from solo.admin import SingletonModelAdmin
# Register your models here.
from allauth.account.models import EmailAddress
from django.contrib.auth.admin import UserAdmin 

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
    list_display = ('id','customer_name','subtotal',)

    def customer_name(self,obj:Order): 
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    customer_name.short_description = "Cliente"

@admin.register(OrderDetail)
class AdminOrderDetail(admin.ModelAdmin):
    pass


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('first_name', 'last_name',
                    'email','email_verified')
    list_display_links = ('first_name','last_name','email')  

    @admin.display(description='Email verificata',boolean=True)
    def email_verified(self,obj):
        return EmailAddress.objects.filter(email=obj.email).first().verified

@admin.register(GeneraliModel)
class AdminGeneraliModel(SingletonModelAdmin):
    pass