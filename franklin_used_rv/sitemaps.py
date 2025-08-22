from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shop.models import Product

class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["home", "about", "shop", "blog"]

    def location(self, item):
        return reverse(item)


class RVSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def location(self, obj):
        return reverse("product", kwargs={"slug": obj.slug, "stock_no": obj.stock_no})

    def lastmod(self, obj):
        return obj.created_at  # optional: needs an updated_at field
