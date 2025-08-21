from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("buy/<int:rv_id>/", views.order_register, name="order_register"),
    path("success/", views.order_success, name="order_success"),
]
