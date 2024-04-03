from django.db import models
from common.mixins.models import (
    UUIDModel,
    TimeStampModel,
    BaseModel,
)


class Category(
        UUIDModel,
        TimeStampModel,
    ):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        to=Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return self.name


class PriceItem(TimeStampModel):
    date = models.DateField()
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='price_items',
    )

    class Meta:
        verbose_name = 'Price Item'
        verbose_name_plural = 'Price Items'
        ordering = ['date']

    def __str__(self) -> str:
        return f'{self.product} - {self.price} - {self.price}'
