from django.urls import path
from .views import (
    CategoryListView,
    DeleteCategoryView,
)


app_name = 'products'


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<str:id>/', DeleteCategoryView.as_view(), name='delete_category'),
]
