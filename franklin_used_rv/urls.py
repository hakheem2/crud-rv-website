from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('pages.urls')),   # home / main pages
    path('buy-used-rv/', include('shop.urls')),
    path('blog/', include('blog.urls')),
    path("orders/", include("orders.urls", namespace="order")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)