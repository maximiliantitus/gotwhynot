from django.contrib import admin
from .models import Product, OrderItem, Home, Order
# Register your models here.



admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Home)
admin.site.register(Order)