from rest_framework.serializers import ModelSerializer
from products.models import Category


class SimpleCategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )
        read_only_fields = fields


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'products',
        )
        read_only_fields = fields
