from rest_framework import serializers
from .models import User, Product, Order, OrderItem, Review, NewsletterSubscriber


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['name', 'phone', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'email', 'role', 'created_at']


class ProductListSerializer(serializers.ModelSerializer):
    """Minimal serializer for home_page.html product grid."""
    image = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'price', 'original_price',
                  'discount_percent', 'badge', 'size', 'image', 'rating_avg', 'rating_count']


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for product.html detail page."""
    image = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'category', 'price', 'original_price', 'discount_percent',
            'badge', 'size', 'colors', 'sizes_available', 'images', 'image',
            'short_description', 'composition', 'care_instructions', 'shipping_info',
            'rating_avg', 'rating_count', 'is_active', 'created_at'
        ]


class ProductAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin.html product management."""
    image = serializers.ReadOnlyField()
    discount_percent = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer_name', 'is_verified_buyer', 'rating', 'title', 'body', 'created_at']
        read_only_fields = ['id', 'created_at']


class OrderItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['product_id', 'title', 'size', 'color', 'quantity', 'unit_price', 'image', 'subtotal']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'governorate', 'address',
            'payment_method', 'subtotal', 'shipping_fee', 'total', 'items'
        ]

    def create(self, validated_data):
        import random
        items_data = validated_data.pop('items')
        order_id = f"BSM-{random.randint(1000, 9999)}"
        while Order.objects.filter(order_id=order_id).exists():
            order_id = f"BSM-{random.randint(1000, 9999)}"
        order = Order.objects.create(order_id=order_id, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
