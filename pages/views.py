from django.shortcuts import render
from shop.models import Product
import random
# Create your views here.

def home(request):
    products = list(Product.objects.all())

    # Random 8 products
    specials = random.sample(products, min(len(products), 8))

    # Last 8 uploads
    latest = Product.objects.order_by('-created_at')[:8]

    context = {
        'specials': specials,
        'latest': latest,
    }
    return render(request, 'index.html', context)

def faqs(request):
    return render(request, 'faqs.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'contract-terms.html')


# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
#
# def order_email(user_email, context):
#     """
#     Send an orders confirmation email to the user.
#     """
#     subject = "Your Order Confirmation - Franklin Used RVs"
#
#     # Render the HTML template
#     html_content = render_to_string('emails/orders-template.html', context)
#
#     # Create the email
#     msg = EmailMultiAlternatives(
#         subject=subject,
#         body='This is a HTML email. Please view it in an HTML compatible email client.',
#         from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings.py
#         to=[user_email],
#     )
#
#     # Attach the HTML content
#     msg.attach_alternative(html_content, "text/html")
#
#     # Send the email
#     msg.send()
