from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_contact_email(data):
    """
    Send contact form message to the site admin email.
    """
    subject = f"New Contact Form Submission from {data['name']}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [settings.DEFAULT_FROM_EMAIL]  # Only send to website email

    html_content = render_to_string("emails/contact_email.html", {
        "name": data["name"],
        "email": data["email"],
        "phone": data["phone"],
        "message": data["message"],
    })

    msg = EmailMultiAlternatives(subject, "", from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
