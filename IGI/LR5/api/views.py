import logging
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import FurnitureItem, FurnitureCategory, Promo
from orders.models import Order
from clients.models import Client
from .serializers import (
    FurnitureItemSerializer, FurnitureCategorySerializer,
    OrderSerializer, ClientSerializer, PromoSerializer
)

logger = logging.getLogger('api')


class FurnitureItemViewSet(viewsets.ModelViewSet):
    queryset = FurnitureItem.objects.select_related('category', 'model').prefetch_related('tags')
    serializer_class = FurnitureItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'product_code', 'description']
    ordering_fields = ['price', 'name', 'created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class FurnitureCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FurnitureCategory.objects.all()
    serializer_class = FurnitureCategorySerializer
    permission_classes = [AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('client', 'manager').prefetch_related('items')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'client']
    search_fields = ['order_number']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        try:
            client = user.client_profile
            return super().get_queryset().filter(client=client)
        except Exception:
            return super().get_queryset().none()


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'is_active']
    search_fields = ['company_name', 'client_code']


class PromoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Promo.objects.filter(is_active=True)
    serializer_class = PromoSerializer
    permission_classes = [AllowAny]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_stats(request):
    from orders.models import OrderItem
    from django.db.models import Sum, Count
    data = {
        'total_orders': Order.objects.count(),
        'delivered_orders': Order.objects.filter(status='delivered').count(),
        'total_clients': Client.objects.count(),
        'total_furniture': FurnitureItem.objects.count(),
        'active_furniture': FurnitureItem.objects.filter(is_active=True).count(),
    }
    return Response(data)
