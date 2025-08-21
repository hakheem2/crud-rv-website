from django.db import models
import random
import string
from decimal import Decimal


def generate_order_id():
    """Generate random unique 5-digit number for order_id"""
    return ''.join(random.choices(string.digits, k=5))


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("paid", "Paid"),
        ("cancelled", "Cancelled"),
    ]

    order_id = models.CharField(max_length=10, unique=True, default=generate_order_id)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    payment_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, null=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total_from_items(self):
        """Calculate total_amount from related OrderItems."""
        total = sum((item.price for item in self.items.all()), Decimal("0.00"))
        self.total_amount = total
        self.save(update_fields=["total_amount"])

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    rv_name = models.CharField(max_length=255)
    stock_no = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    mileage = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.rv_name} ({self.stock_no}) - Order {self.order.order_id}"
