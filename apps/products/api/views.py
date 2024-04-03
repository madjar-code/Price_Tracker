from enum import Enum
from uuid import UUID
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
)
from drf_yasg.utils import swagger_auto_schema

from products.models import (
    Category,
)
from .serializers import (
    SimpleCategorySerializer,
)


class ErrorMessages(str, Enum):
    NO_CATEGORY = 'Category with `id` not found'
    NO_PRODUCT = 'Category with `id` not found'


class CategoryListView(ListAPIView):
    serializer_class = SimpleCategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(operation_id='all_categories')
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


class DeleteCategoryView(DestroyAPIView):
    serializer_class = SimpleCategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(operation_id='delete_category')
    def delete(self, request: Request, id: UUID) -> Response:
        category: Category = self.queryset.filter(id=id).first()
        if not category:
            return Response(
                {'error': ErrorMessages.NO_CATEGORY},
                status.HTTP_404_NOT_FOUND,
            )
        category.delete()
        return Response(
            {'message': 'Deletion complete!'},
            status.HTTP_204_NO_CONTENT,
        )
