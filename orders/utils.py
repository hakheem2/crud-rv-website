from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_order_confirmation_email(order):
    """
    Send confirmation email to user after order submission.
    Notes field can be empty.
    """
    subject = f"Order Confirmation | OR-{order.order_id}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.email]

    html_content = render_to_string(
        "order_template.html",
        {
            "order": order,
            "website_url": "https://franklinusedrvs.com",
            "year": order.created_at.year,
            "notes": order.notes or "",  # Pass empty string if notes is None or blank
        },
    )

    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
