from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs
    path('', include('pages.urls')),   # home / main pages
    path('buy-used-rv/', include('shop.urls')),
    path('blog/', include('blog.urls')),
]

from django.conf import settings
from django.conf.urls.static import static
import os
from pathlib import Path

if settings.DEBUG or os.environ.get('RAILWAY_STATIC_SERVE_MEDIA') == 'True':
    BASE_DIR = Path(__file__).resolve().parent.parent
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
