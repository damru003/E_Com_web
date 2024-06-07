from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','image')
    
admin.site.register(Product, ProductAdmin)

admin.site.register(Category)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','phone','email')

admin.site.register(Customer, CustomerAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('product','customer','quantity','price','date')

admin.site.register(Order, OrderAdmin)