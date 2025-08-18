from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<slug:slug>/<int:stock_no>/', views.product, name='product'),
    path('sales-rebates/', views.sales_rebates, name='sales_rebates'),
    path('ajax/sort-products/', views.ajax_sort_products, name='ajax_sort_products'),
    path('ajax/filter-products/', views.ajax_filter_products, name='ajax_filter_products'),
    path('ajax/filter-sort-products/', views.ajax_filter_sort_products, name='ajax_filter_sort_products'),
]
