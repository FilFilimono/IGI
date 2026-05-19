from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'api'

router = DefaultRouter()
router.register(r'furniture', views.FurnitureItemViewSet)
router.register(r'categories', views.FurnitureCategoryViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'promos', views.PromoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token'),
    path('stats/', views.api_stats, name='api_stats'),
]
