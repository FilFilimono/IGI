from rest_framework import serializers
from catalog.models import FurnitureItem, FurnitureCategory, Tag, Promo
from orders.models import Order, OrderItem
from clients.models import Client


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class FurnitureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FurnitureCategory
        fields = ['id', 'name', 'slug', 'description']


class FurnitureItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    model_name = serializers.CharField(source='model.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = FurnitureItem
        fields = ['id', 'product_code', 'name', 'category', 'category_name',
                  'model', 'model_name', 'price', 'is_active', 'description',
                  'weight', 'dimensions', 'material', 'tags', 'image', 'created_at']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_code', 'company_name', 'phone', 'city', 'address',
                  'email', 'contact_person', 'is_active']


class OrderItemSerializer(serializers.ModelSerializer):
    furniture_name = serializers.CharField(source='furniture.name', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'furniture', 'furniture_name', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source='client.company_name', read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'client', 'client_name', 'order_date', 'due_date',
                  'status', 'notes', 'items', 'total_amount']


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['id', 'code', 'discount_type', 'discount_value', 'description',
                  'valid_from', 'valid_to', 'usage_limit', 'used_count']
