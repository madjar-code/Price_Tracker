from django.urls import path
from .views import (
    CategoryListView,
    CreateCategoryView,
    DeleteCategoryView,
    UpdateCategoryView,

    ProductListView,
    ProductDetailsView,
    DeleteProductView,
    UpdateProductView,
    CreateProductView,

    SetPriceForPeriodView,
    GetPriceForPeriodView,
)


app_name = 'products'


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CreateCategoryView.as_view(), name='create_category'),
    path('categories/update/<str:id>/', UpdateCategoryView.as_view(), name='update_category'),
    path('categories/delete/<str:id>/', DeleteCategoryView.as_view(), name='delete_category'),

    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', CreateProductView.as_view(), name='create_product'),
    path('products/update/<str:id>/', UpdateProductView.as_view(), name='update_product'),
    path('products/delete/<str:id>/', DeleteProductView.as_view(), name='delete_product'),
    path('products/<str:id>/', ProductDetailsView.as_view(), name='product_details'),

    path('prices/products/set-price/', SetPriceForPeriodView.as_view(), name='set_price_for_period'),
    path('prices/products/get-price/<str:id>/', GetPriceForPeriodView.as_view(), name='get_avg_price_for_period'),
]
