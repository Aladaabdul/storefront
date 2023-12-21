from itertools import count
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count
from . import models

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','featured_product', 'products_count']
    list_per_page = 10
    ordering = ["title"]
    list_editable = ["featured_product"]

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('featured_product'))
                                                      

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    ordering = ['first_name','last_name']    

admin.site.register(models.Product)

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']

    def customer(self, order):
        return order.customer