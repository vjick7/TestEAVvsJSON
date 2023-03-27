from django.urls import path, re_path, include
from . import views

#router = routers.DefaultRouter()
#router.register(r'category/', views.category_api_views, basename='category_api_views')

app_name = 'eav_products'



urlpatterns = [
    path('', views.category_list, name='product_list'),
    path('<str:category_url>/', views.product_list, name='product_list_by_category'),
]