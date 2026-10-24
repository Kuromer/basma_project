from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # مسارات صفحات الفرونت إند
    path('', TemplateView.as_view(template_name='home_page.html'), name='root'),
    path('home_page.html', TemplateView.as_view(template_name='home_page.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='home_page.html'), name='index'),
    path('product.html', TemplateView.as_view(template_name='product.html'), name='product'),
    path('checkout.html', TemplateView.as_view(template_name='checkout.html'), name='checkout'),
    path('signup.html', TemplateView.as_view(template_name='signup.html'), name='signup'),
    path('admin.html', TemplateView.as_view(template_name='admin.html'), name='admin_panel'),
]