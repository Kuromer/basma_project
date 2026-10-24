from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import User, Product, Order, Review, NewsletterSubscriber
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, UserSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductAdminSerializer,
    ReviewSerializer, OrderCreateSerializer, OrderSerializer,
    NewsletterSerializer
)


# ─── AUTH ─────────────────────────────────────────────────────────────────────

@api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})


# ─── PRODUCTS (PUBLIC) ────────────────────────────────────────────────────────

@api_view(['GET'])
def product_list(request):
    """
    GET /api/products/
    Query params: ?category=dresses&search=linen
    """
    products = Product.objects.filter(is_active=True)

    category = request.query_params.get('category')
    if category and category != 'all':
        products = products.filter(category=category)

    search = request.query_params.get('search')
    if search:
        products = products.filter(
            Q(title__icontains=search) | Q(category__icontains=search)
        )

    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    """GET /api/products/<id>/"""
    try:
        product = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def product_related(request, pk):
    """GET /api/products/<id>/related/ — same category, exclude self"""
    try:
        product = Product.objects.get(pk=pk, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    related = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=pk)[:4]
    serializer = ProductListSerializer(related, many=True)
    return Response(serializer.data)


# ─── REVIEWS ─────────────────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def product_reviews(request, pk):
    """GET/POST /api/products/<id>/reviews/"""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        reviews = product.reviews.all().order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            # Recalculate rating
            all_reviews = product.reviews.all()
            if all_reviews.exists():
                product.rating_avg = round(
                    sum(r.rating for r in all_reviews) / all_reviews.count(), 1
                )
                product.rating_count = all_reviews.count()
                product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── ORDERS ──────────────────────────────────────────────────────────────────

@api_view(['POST'])
def create_order(request):
    """POST /api/orders/"""
    serializer = OrderCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user if request.user.is_authenticated else None
        order = serializer.save(user=user)
        return Response({
            'order_id': order.order_id,
            'status': order.status,
            'total': str(order.total)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def order_detail(request, order_id):
    """GET /api/orders/<order_id>/"""
    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)


# ─── NEWSLETTER ───────────────────────────────────────────────────────────────

@api_view(['POST'])
def newsletter_subscribe(request):
    """POST /api/newsletter/subscribe/"""
    serializer = NewsletterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        _, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if created:
            return Response({'message': 'Subscribed successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already subscribed.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─── ADMIN ───────────────────────────────────────────────────────────────────

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """GET /api/admin/stats/"""
    return Response({
        'total_products': Product.objects.filter(is_active=True).count(),
        'categories_count': Product.objects.filter(is_active=True).values('category').distinct().count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_product_list(request):
    """GET/POST /api/admin/products/"""
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductAdminSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_product_detail(request, pk):
    """GET/PUT/DELETE /api/admin/products/<id>/"""
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductAdminSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductAdminSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
