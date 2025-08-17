from django.contrib import admin
from .models import Product, Gallery

# Register your models here.
class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 12  # This creates 5 empty gallery fields by default
    min_num = 0  # Minimum number of gallery images
    max_num = None  # No limit, you can add more dynamically

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stock_no', 'year', 'sale_price', 'mileage', 'engine', 'created_at')
    inlines = [GalleryInline]
