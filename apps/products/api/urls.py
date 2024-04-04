from django.urls import path
from .views import (
    CategoryListView,
    CreateCategoryView,
    DeleteCategoryView,
    UpdateCategoryView,

    ProductListView,
)


app_name = 'products'


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CreateCategoryView.as_view(), name='create_category'),
    path('categories/update/<str:id>/', UpdateCategoryView.as_view(), name='update_category'),
    path('categories/<str:id>/', DeleteCategoryView.as_view(), name='delete_category'),

    path('products/', ProductListView.as_view(), name='product_list'),
]
