from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderItem


# Inline for OrderItems
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

    # Auto-update total_amount after saving inlines
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_from_items()

    # Admin actions with email notification
    def mark_as_confirmed(self, request, queryset):
        updated = 0
        for order in queryset:
            order.status = "confirmed"
            order.save()
            send_status_email(order)
            updated += 1
        self.message_user(request, f"{updated} order(s) marked as confirmed and emailed.")
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"

    def mark_as_paid(self, request, queryset):
        updated = 0
        for order in queryset:
            order.status = "paid"
            order.save()
            send_status_email(order)
            updated += 1
        self.message_user(request, f"{updated} order(s) marked as paid and emailed.")
    mark_as_paid.short_description = "Mark selected orders as Paid"

    def mark_as_cancelled(self, request, queryset):
        updated = 0
        for order in queryset:
            order.status = "cancelled"
            order.save()
            send_status_email(order)
            updated += 1
        self.message_user(request, f"{updated} order(s) marked as cancelled and emailed.")
    mark_as_cancelled.short_description = "Mark selected orders as Cancelled"