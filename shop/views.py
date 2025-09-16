from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Product
import random
from django.db.models import F
from django.db.models import Max, Min
from django.http import JsonResponse
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
    initial_products = products
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


def us_inventory(request):
    products = Product.objects.filter(country="USA")

    # distinct fields
    product_names = products.values_list("name", flat=True).distinct()
    product_years = products.values_list("year", flat=True).distinct().order_by("year")
    product_locations = products.values_list("location", flat=True).distinct()
    # max and min price
    max_price = products.aggregate(Max("sale_price"))["sale_price__max"]
    min_price = products.aggregate(Min("sale_price"))["sale_price__min"]

    context = {
        "products": products,
        "max_price": max_price,
        "min_price": min_price,
        "product_names": product_names,
        "product_years": product_years,
        "product_locations": product_locations,
    }
    return render(request, 'us-inventory.html', context)


def canada_inventory(request):
    products = Product.objects.filter(country="Canada")

    # distinct fields
    product_names = products.values_list("name", flat=True).distinct()
    product_years = products.values_list("year", flat=True).distinct().order_by("year")
    product_locations = products.values_list("location", flat=True).distinct()
    # max and min price
    max_price = products.aggregate(Max("sale_price"))["sale_price__max"]
    min_price = products.aggregate(Min("sale_price"))["sale_price__min"]

    context = {
        "products": products,
        "max_price": max_price,
        "min_price": min_price,
        "product_names": product_names,
        "product_years": product_years,
        "product_locations": product_locations,
    }
    return render(request, 'canada-inventory.html', context)


def sales_rebates(request):
    return render(request, 'sales-rebates.html')


def ajax_filter_sort_products(request):
    # Get filter params
    model = request.GET.get('model', 'all_models')
    year = request.GET.get('year', 'all_years')
    location = request.GET.get('location', 'all_locations')
    price = request.GET.get('price', None)
    sort_key = request.GET.get('sort', 'all')

    # Start with all products
    products = Product.objects.all()

    # Apply filters
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
            pass

    # Apply sorting
    if sort_key == 'recent':
        products = products.order_by('-created_at')
    elif sort_key == 'model':
        products = products.order_by('-year')
    elif sort_key == 'lowest_price':
        products = products.order_by('sale_price')
    elif sort_key == 'highest_price':
        products = products.order_by('-sale_price')
    elif sort_key == 'mileage':
        products = products.order_by('mileage')
    elif sort_key == 'all':
        all_products = list(products)
        products = random.sample(all_products, min(len(all_products), 8))

    return render(request, 'partials/product_list.html', {'products': products})


def toggle_wishlist(request):
    if request.method == "POST":
        product_id = str(request.POST.get("product_id"))

        # Initialize wishlist if not available
        wishlist = request.session.get("wishlist", [])

        if product_id in wishlist:
            wishlist.remove(product_id)
            in_wishlist = False
        else:
            wishlist.append(product_id)
            in_wishlist = True

        request.session["wishlist"] = wishlist
        request.session.modified = True

        return JsonResponse({
            "success": True,
            "in_wishlist": in_wishlist,
        })

    return JsonResponse({"success": False}, status=400)


def wishlist_page(request):
    wishlist = request.session.get("wishlist", [])
    products = Product.objects.filter(id__in=wishlist)
    return render(request, "wishlist.html", {"products": products})
