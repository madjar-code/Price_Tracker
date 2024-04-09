from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID
from django.db.models import Avg
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,
    GenericAPIView,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from products.models import (
    Category,
    Product,
    PriceItem,
)
from .serializers import (
    SimpleCategorySerializer,
    UpdateCategorySerializer,
    SimpleProductSerializer,
    ProductSerializer,
    UpdateCreateProductSerializer,

    SetPriceForPeriodSerializer,
)


class ErrorMessages(str, Enum):
    NO_CATEGORY = 'Category with given `id` not found'
    NO_PRODUCT = 'Product with given `id` not found'
    INVALID_DATE_FORMAT = 'Invalid date format. Date format should be YYYY-MM-DD.'
    BOTH_DATES_REQUIRED = 'Both start_date and end_date are required as query parameters.'
    DATE_ORDER_ERROR = 'End date must be after start date'


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


class ProductListView(ListAPIView):
    serializer_class = SimpleProductSerializer
    queryset = Product.active_objects.all()

    @swagger_auto_schema(operation_id='all_products')
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


class ProductDetailsView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.active_objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(operation_id='product_details')
    def get(self, request: Request, id: UUID) -> Response:
        product: Product | None = self.queryset.filter(id=id).first()
        if not product:
            return Response(
                {'error': ErrorMessages.NO_PRODUCT},
                status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(instance=product)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateProductView(CreateAPIView):
    serializer_class = UpdateCreateProductSerializer

    @swagger_auto_schema(operation_id='create_product')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UpdateProductView(GenericAPIView):
    serializer_class = UpdateCreateProductSerializer
    queryset = Product.active_objects.all()

    @swagger_auto_schema(operation_id='update_product')
    def patch(self, request: Request, id: UUID) -> Response:
        product: Product | None = self.queryset.filter(id=id).first()
        if not product:
            return Response(
                {'error': ErrorMessages.NO_PRODUCT},
                status.HTTP_404_NOT_FOUND,
            )
        serializer = self.serializer_class(
            instance=product,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK,
        )


class DeleteProductView(DestroyAPIView):
    queryset = Product.active_objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(operation_id='delete_product')
    def delete(self, request: Request, id: UUID) -> Response:
        product: Product | None = self.queryset.filter(id=id).first()
        if not product:
            return Response(
                {'error': ErrorMessages.NO_PRODUCT},
                status.HTTP_404_NOT_FOUND,
            )
        product.delete()
        return Response(
            {'message': 'Deletion complete!'},
            status.HTTP_204_NO_CONTENT,
        )


class SetPriceForPeriodView(GenericAPIView):
    serializer_class = SetPriceForPeriodSerializer

    @swagger_auto_schema(
        operation_id='set_price_for_period',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_UUID,
                    example='5f25912c-1687-488f-8f4b-d9e18628fdaa'
                ),
                'start_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE
                ),
                'end_date': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATE
                ),
                'price': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    format=openapi.FORMAT_DECIMAL
                )
            },
            required=[
                'product_id',
                'start_date',
                'end_date',
                'price'
            ]
        )
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Price was set for a period!'},
            status.HTTP_201_CREATED, 
        )


class GetPriceForPeriodView(APIView):
    @swagger_auto_schema(
        operation_id='get_avg_price_for_period',
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='Start Date for Count Average Price',
            ),
            openapi.Parameter(
                'end_date',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description='End Date for Count Average Price',
            ),
        ]
    )
    def get(self, request: Request, id: UUID) -> Response:
        product: Product | None =\
            Product.active_objects.filter(id=id).first()

        if not product:
            return Response(
                {'error': ErrorMessages.NO_PRODUCT},
                status=status.HTTP_404_NOT_FOUND,
            )

        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return Response(
                {'error': ErrorMessages.BOTH_DATES_REQUIRED},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            start_date = datetime.strptime(
                start_date_str, '%Y-%m-%d'
            ).date()
            end_date = datetime.strptime(
                end_date_str, '%Y-%m-%d'
            ).date()
        except ValueError:
            return Response(
                {'error': ErrorMessages.INVALID_DATE_FORMAT},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if end_date < start_date:
            return Response(
                {'error': ErrorMessages.DATE_ORDER_ERROR},
                status=status.HTTP_400_BAD_REQUEST,
            )

        average_price = PriceItem.objects.filter(
            product=product,
            date__range=[start_date, end_date]
        ).aggregate(avg_price=Avg('price'))

        average_price: Decimal | None = average_price['avg_price']

        if average_price is not None:
            average_price = round(average_price, 2)

        return Response(
            {'average_price': average_price},
            status=status.HTTP_200_OK,
        )
