from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('us/', views.us_inventory, name='us_inventory'),
    path('canada/', views.canada_inventory, name='canada_inventory'),
    path('<slug:slug>/<int:stock_no>/', views.product, name='product'),
    path('sales-rebates/', views.sales_rebates, name='sales_rebates'),
    path('ajax/filter-sort-products/', views.ajax_filter_sort_products, name='ajax_filter_sort_products'),
    path("wishlist/toggle/", views.toggle_wishlist, name="toggle_wishlist"),
    path("wishlist/", views.wishlist_page, name="wishlist_page"),
]
