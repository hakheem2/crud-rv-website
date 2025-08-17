from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product
import random
from django.db.models import F
from django.db.models import Max, Min
# Create your views here.


def shop(request):
    products = list(Product.objects.all())

    # distinct names
    product_names = Product.objects.values_list("name", flat=True).distinct()
    # distinct years
    product_years = Product.objects.values_list("year", flat=True).distinct().order_by("year")
    # distinct locations
    product_locations = Product.objects.values_list("location", flat=True).distinct()
    #radom initial products
    initial_products = random.sample(products, min(len(products), 8))
    #maxed price
    max_price = Product.objects.aggregate(Max("sale_price"))["sale_price__max"]
    #min price
    min_price = Product.objects.aggregate(Min("sale_price"))["sale_price__min"]

    context = {
        "products": initial_products,
        "max_price": max_price,
        "min_price": min_price,
        "product_names": product_names,
        "product_years": product_years,
        "product_locations": product_locations,
    }
    return render(request, 'shop.html', context)


def product(request, slug, stock_no):
    product = get_object_or_404(Product, slug=slug, stock_no=stock_no)
    context = {'product': product}
    return render(request, 'product.html', context)


def sales_rebates(request):
    return render(request, 'sales-rebates.html')


def ajax_sort_products(request):
    sort_key = request.GET.get('sort', 'all')
    products = Product.objects.all()
    all_products = list(Product.objects.all())

    if sort_key == 'all':
        products = random.sample(all_products, min(len(all_products), 8))
    elif sort_key == 'recent':
        products = products.order_by('-created_at')
    elif sort_key == 'model':
        products = products.order_by('-year')  # or your model logic
    elif sort_key == 'lowest_price':
        products = products.order_by('sale_price')
    elif sort_key == 'highest_price':
        products = products.order_by('-sale_price')
    elif sort_key == 'mileage':
        products = products.order_by('mileage')

    return render(request, 'partials/product_list.html', {'products': products})


def ajax_filter_products(request):
    # Get filter parameters
    model = request.GET.get('model', 'all_models')
    year = request.GET.get('year', 'all_years')
    location = request.GET.get('location', 'all_locations')
    price = request.GET.get('price', None)

    # Start with all products
    products = Product.objects.all()

    # Apply filters if not default
    if model != 'all_models':
        products = products.filter(name=model)

    if year != 'all_years':
        products = products.filter(year=year)

    if location != 'all_locations':
        products = products.filter(location=location)

    if price:
        try:
            price = float(price)
            products = products.filter(sale_price__lte=price)
        except ValueError:
            pass  # Ignore invalid price

    # Return partial template for AJAX
    return render(request, 'partials/product_list.html', {'products': products})