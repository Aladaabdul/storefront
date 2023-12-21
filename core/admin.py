from django.contrib import admin
from tags.models import TagItem
from store.models import Product
from store.admin import ProductAdmin, ProductImageInline
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.

class TagInLine(GenericTabularInline):
    model = TagItem

class CustomProductAdmin(ProductAdmin):
    inlines = [TagInLine, ProductImageInline]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)