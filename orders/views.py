from django.shortcuts import get_object_or_404, render, redirect
from django.db import transaction
from .models import Order, OrderItem
from .forms import OrderForm
from .utils import send_order_confirmation_email
from shop.models import Product  # Your RV product model
from django.urls import reverse
from decimal import Decimal


def order_register(request, rv_id):
    """
    Handle order form submission for a specific RV.
    Ensures email is sent reliably, total_amount is calculated,
    and notes field can be empty.
    """
    product = get_object_or_404(Product, id=rv_id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create the Order object
                    order = form.save(commit=False)
                    order.status = "pending"  # Status remains
                    order.total_amount = Decimal("0.00")
                    order.save()

                    # Create OrderItem linked to this order
                    OrderItem.objects.create(
                        order=order,
                        rv_name=product.name,
                        stock_no=product.stock_no,
                        price=product.price,
                        mileage=product.mileage,
                        year=product.year,
                    )

                    # Update total_amount from items
                    order.update_total_from_items()

                    # Send confirmation email
                    order.notes = order.notes or ""
                    send_order_confirmation_email(order)

                # Redirect to success page with order_id
                return redirect(f"{reverse('order:order_success')}?order_id={order.order_id}")

            except Exception as e:
                print("Error during order submission:", e)
                form.add_error(None, "An error occurred while submitting your order. Please try again.")

    else:
        form = OrderForm()

    return render(request, "order_register.html", {"form": form, "product": product})


def order_success(request):
    """
    Display success page after order submission
    """
    order_id = request.GET.get("order_id")
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, "order_success.html", {"order": order})
