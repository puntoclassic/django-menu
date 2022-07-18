from decimal import Decimal
from django.db import models
from impostazioni.models import User
from django.db.models import Sum

# Create your models here.

class OrderStatus(models.Model):
    description = models.CharField(verbose_name='Descrizione stato',max_length=255,blank=False,null=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "stato ordine"
        verbose_name_plural = "stati ordine"

class Order(models.Model):
    customer = models.ForeignKey(User,related_name='orders',verbose_name="Cliente",blank=False,null=True,on_delete=models.SET_NULL)
    shipping_address = models.TextField(verbose_name='Indirizzo di consegna',blank=True,null=True)
    shipping_delivery_time = models.TextField(verbose_name='Orario di consegna',blank=True,null=True)
    shipping_required = models.BooleanField(verbose_name='Consegna a domicilio',default=False)
    order_status = models.ForeignKey(OrderStatus,blank=False,null=True,on_delete=models.SET_NULL,verbose_name='Stato ordine')
    note = models.TextField(blank=True,null=True,verbose_name='Note ordine')
    is_paid = models.BooleanField(verbose_name='Pagato',default=False)

  
    @property
    def subtotal(self):
        total = self.order_details.aggregate(TOTAL = Sum('price'))['TOTAL']
        return total 

    
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "ordine"
        verbose_name_plural = "ordini"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,related_name="order_details",verbose_name='Ordine',blank=False,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=False,default=1)
    unit_price =  models.DecimalField(verbose_name='Prezzo unitario', max_digits=4, decimal_places=2,blank=True,null=False)
    price =  models.DecimalField(verbose_name='Prezzo totale', max_digits=4, decimal_places=2,blank=True,null=False) 

    def save(self, *args, **kwargs) -> None:
        
        self.price = self.unit_price * self.quantity
       
        return super().save(*args, **kwargs)  

    
    def __str__(self):
        return f"{str(self.order.id)} - {self.name}"

    class Meta:
        verbose_name = "dettaglio ordine"
        verbose_name_plural = "dettagli ordini"
