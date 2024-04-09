from django.contrib import admin
from common.mixins.admin import ReadOnlyFieldsAdmin
from .models import (
    Category,
    Product,
    PriceItem,
)


class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1


@admin.register(Product)
class ProductAdmin(ReadOnlyFieldsAdmin):
    list_display = (
        'id',
        'name',
        'sku',
        'category',
    )
    inlines = [PriceItemInline]


@admin.register(Category)
class CategoryAdmin(ReadOnlyFieldsAdmin):
    list_display = (
        'id',
        'name',
        'updated_at',
        'created_at',
    )
    list_display_links = (
        'id',
        'name',
    )
