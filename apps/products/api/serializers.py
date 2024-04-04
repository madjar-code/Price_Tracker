from typing import List, Dict
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from products.models import (
    Category,
    Product,
    PriceItem,
)


class SimpleCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class UpdateCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'updated_at',
            'created_at',
        )
        read_only_fields = (
            'id',
            'updated_at',
            'created_at',
        )


class PriceItemSerializer(ModelSerializer):
    class Meta:
        model = PriceItem
        fields = (
            'date',
            'price',
        )
        read_only_fields = fields


class SimpleProductSerializer(ModelSerializer):
    category_name = SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category_name',
            'sku',
        )
        read_only_fields = fields

    def get_category_name(self, obj: Product) -> str | None:
        if obj.category:
            return obj.category.name
        return None


class ProductSerializer(ModelSerializer):
    category = SimpleCategorySerializer()
    price_items = SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'category',
            'sku',
            'description',
            'price_items',
        )
        read_only_fields = fields

    def get_price_items(self, obj: Product) -> List[Dict[str, str]]:
        price_items = obj.price_items.all().order_by('-date')
        serializer = PriceItemSerializer(price_items, many=True)
        return serializer.data
