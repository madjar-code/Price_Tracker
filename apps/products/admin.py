from django.contrib import admin

from .models import (
    Category,
    Product,
    PriceItem,
)


class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
    )
    inlines = [PriceItemInline]
