from itertools import count
from typing import Any, List, Optional, Tuple
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models import Count
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset):
        if self.value == '<10':
            return queryset.filter(Inventory__lt = 10)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','featured_product', 'products_count']
    list_per_page = 10
    ordering = ["title"]
    list_editable = ["featured_product"]
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
        + '?'
        + urlencode({
            'collection__id': str(collection.id)
        }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('title'))
                                                      

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','Display_order']
    list_editable = ['membership']
    list_select_related = ["user"]
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartwith']
    autocomplete_fields = ['user']

    @admin.display(ordering='Display_order')
    def Display_order(self,customer):
        url = (
            reverse("admin:store_order_changelist")
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{}</a>',url,customer.Display_order)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(Display_order = Count(OrderAdmin))

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    # Add thumbnail to uploaded image
    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(f'<img src="{instance.image.url}" class="thunbnail" />')
        return ''

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear inventory']
    inlines = [ProductImageInline]
    list_display = ['title','inventory','description']
    ordering = ['title']
    list_filter = ['title', 'last_update', InventoryFilter]
    search_fields = ['title']

    @admin.action(description='clear inventory')
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(
            request,
            f'{updated_count}Product Successfully Updated'
        )

    class Media:
        css = {
            "all" : ['store/styles.css']
        }

class OrderItemInLine(admin.StackedInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInLine]
    list_display = ['id', 'placed_at', 'customer']

    def customer(self, Order):
        return Order.customer