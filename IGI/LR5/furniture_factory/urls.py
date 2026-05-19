from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('employees/', include('employees.urls', namespace='employees')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/', include('api.urls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
