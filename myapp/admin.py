# myapp/admin.py

from django.contrib import admin
from .models import Buyer, Seller, Product, Bid, Deal

admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Deal)
