from uuid import UUID
from datetime import (
    datetime,
    timedelta,
)
from enum import Enum
from typing import (
    Any,
    List,
    Dict,
    NoReturn
)
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
)
from products.models import (
    Category,
    Product,
    PriceItem,
)


class ErrorMessages(str, Enum):
    NO_CATEGORY = 'Category with given `name` not found'
    DATE_ERROR = 'End date must be after start date'
    NO_PRODUCT = 'Product with given `id` not found'


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


class UpdateCreateProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'sku',
            'description',
            'category',
            'is_active',
            'updated_at',
            'created_at',
        )
        read_only_fields = (
            'id',
            'is_active',
            'updated_at',
            'created_at',
        )


class SetPriceForPeriodSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    price = serializers.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    def create_update_price_items(
            self,
            product_id: UUID,
            start_date: datetime,
            end_date: datetime,
            price: float
        ) -> None:
        product = Product.active_objects.get(id=product_id)

        price_items: QuerySet[PriceItem] = PriceItem.objects.filter(
            product=product,
            date__range=[start_date, end_date],
        )
        existing_price_items: Dict[datetime, PriceItem] = {
            item.date: item for item in price_items
        }
        new_price_items: List[PriceItem] = list()

        for date in self.date_range(start_date, end_date):
            if date in existing_price_items:
                existing_price_items[date].price = price
            else:
                new_price_items.append(PriceItem(
                    product=product,
                    date=date,
                    price=price
                ))

        if existing_price_items:
            PriceItem.objects.bulk_update(
                existing_price_items.values(),
                ['price']
            )
        if new_price_items:
            PriceItem.objects.bulk_create(new_price_items)

    def date_range(
            self,
            start_date: datetime,
            end_date: datetime,
        ):
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

    def validate_product_id(self, value: str) -> NoReturn | str:
        product = Product.objects.filter(id=value).first()
        if not product:
            raise ValidationError(ErrorMessages.NO_PRODUCT.value)
        return value

    def validate(self, attrs: Dict[str, Any]):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError(ErrorMessages.DATE_ERROR.value)
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        product_id = validated_data['product_id']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        price = validated_data['price']

        self.create_update_price_items(product_id, start_date, end_date, price)
        return validated_data
