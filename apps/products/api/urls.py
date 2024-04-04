from django.urls import path
from .views import (
    CategoryListView,
    CreateCategoryView,
    DeleteCategoryView,
    UpdateCategoryView,
)


app_name = 'products'


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CreateCategoryView.as_view(), name='create_category'),
    path('categories/update/<str:id>/', UpdateCategoryView.as_view(), name='update_category'),
    path('categories/<str:id>/', DeleteCategoryView.as_view(), name='delete_category'),
]
