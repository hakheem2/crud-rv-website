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

def where(request):
    return render(request, 'where.html')

def faqs(request):
    return render(request, 'faqs.html')

def about(request):
    return render(request, 'about.html')

def terms(request):
    return render(request, 'contract-terms.html')
