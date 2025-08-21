
#starts here
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ("rv_name", "stock_no", "price", "mileage", "year")
    extra = 0


def send_status_email(order):
    """Send email to user when status changes"""
    subject = f"Order | OR-{order.order_id} Status Update"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    html_content = render_to_string(
        "order_status_template.html",
        {
            "order": order,
            "website_url": "https://franklinusedrvs.com",
            "notes": order.notes or "",
        },
    )

    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

    list_display = (
        "order_id",
        "name",
        "email",
        "phone_number",
        "payment_type",
        "status",
        "total_amount",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "payment_type", "created_at")
    search_fields = ("order_id", "name", "email", "phone_number", "items__rv_name", "items__stock_no")
    readonly_fields = ("order_id", "total_amount", "created_at", "updated_at")
    ordering = ("-created_at",)

    # Remove bulk status actions
    actions = []

    # Auto-update total_amount after saving inlines
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_from_items()

    # Trigger status email on single order save
    def save_model(self, request, obj, form, change):
        if change:  # editing existing order
            old_order = Order.objects.get(pk=obj.pk)
            if old_order.status != obj.status:  # status has changed
                super().save_model(request, obj, form, change)
                send_status_email(obj)
                return
        super().save_model(request, obj, form, change)
