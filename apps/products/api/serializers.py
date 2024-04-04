from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from products.models import (
    Category,
    Product,
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
