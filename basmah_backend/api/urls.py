from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),

    # Products (public)
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/related/', views.product_related, name='product-related'),
    path('products/<int:pk>/reviews/', views.product_reviews, name='product-reviews'),

    # Orders
    path('orders/', views.create_order, name='create-order'),
    path('orders/<str:order_id>/', views.order_detail, name='order-detail'),

    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter-subscribe'),

    # Admin
    path('admin/stats/', views.admin_stats, name='admin-stats'),
    path('admin/products/', views.admin_product_list, name='admin-product-list'),
    path('admin/products/<int:pk>/', views.admin_product_detail, name='admin-product-detail'),
]
