from django.shortcuts import render, redirect
from shop.models import Product
import random
from django.urls import reverse
from .forms import ContactForm
from .utils import send_contact_email
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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Grab cleaned data
            data = form.cleaned_data

            try:
                send_contact_email(data)
            except Exception as e:
                import logging
                logging.exception("Failed to send order confirmation email")

            return redirect(reverse("contact_success"))
    else:
        form = ContactForm()

    return render(request, "about.html", {"form": form})


def terms(request):
    return render(request, 'contract-terms.html')


def contact_success(request):
    return render(request, "emails/contact_success.html")
