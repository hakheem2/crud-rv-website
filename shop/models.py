from django.db import models
from django.utils.text import slugify
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock_no = models.CharField(max_length=50, unique=True)
    mileage = models.IntegerField()
    engine = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    vin_number = models.CharField("VIN", max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/main_images/')


    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    # Add formatted price properties
    @property
    def formatted_price(self):
        return f"{int(self.price):,}"

    @property
    def formatted_sale_price(self):
        if self.sale_price:
            return f"{int(self.sale_price):,}"
        return None


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='uploads/gallery_images/')

    def __str__(self):
        return f"{self.product.name} - Gallery Image"