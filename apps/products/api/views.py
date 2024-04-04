from enum import Enum
from uuid import UUID
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    CreateAPIView,
    GenericAPIView,
)
from drf_yasg.utils import swagger_auto_schema

from products.models import (
    Category,
)
from .serializers import (
    SimpleCategorySerializer,
    UpdateCategorySerializer,
)


class ErrorMessages(str, Enum):
    NO_CATEGORY = 'Category with given `id` not found'
    NO_PRODUCT = 'Product with given `id` not found'


class CategoryListView(ListAPIView):
    serializer_class = SimpleCategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(operation_id='all_categories')
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


class DeleteCategoryView(DestroyAPIView):
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


class UpdateCategoryView(GenericAPIView):
    serializer_class = UpdateCategorySerializer
    queryset = Category.objects.all()

    @swagger_auto_schema(operation_id='update_category')
    def put(self, request: Request, id: UUID) -> Response:
        category: Category | None = self.queryset.filter(id=id).first()
        if not category:
            return Response(
                {'error': ErrorMessages.NO_CATEGORY},
                status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(
            instance=category,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateCategoryView(CreateAPIView):
    serializer_class = SimpleCategorySerializer

    @swagger_auto_schema(operation_id='create_category')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )
