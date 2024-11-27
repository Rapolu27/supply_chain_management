from django.contrib import admin
from .models import Product, PurchaseOrder, Inventory, Supplier
# Register your models here.
admin.site.register(PurchaseOrder)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Supplier)