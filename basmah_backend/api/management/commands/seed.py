from django.core.management.base import BaseCommand
from api.models import Product, User, Review
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Seed the database with initial BASMAH store data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create admin user
        if not User.objects.filter(email='admin@basmah.com').exists():
            admin = User.objects.create_superuser(
                email='admin@basmah.com',
                password='admin123',
                name='BASMAH Admin',
                role='admin'
            )
            admin.is_staff = True
            admin.save()
            Token.objects.get_or_create(user=admin)
            self.stdout.write(self.style.SUCCESS('[OK] Admin user created: admin@basmah.com / admin123'))

        # Create products matching exactly the 6 hardcoded products from home_page.html
        products_data = [
            {
                'title': 'Oversized Linen Shirt Dress',
                'category': 'dresses',
                'price': 89.00,
                'original_price': 120.00,
                'badge': 'Best Seller',
                'size': 'S / M / L',
                'colors': ['Natural Taupe', 'Dark Coffee', 'Cream White', 'Sage Green'],
                'sizes_available': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
                'images': [
                    'https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=400',
                    'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400',
                    'https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=400',
                    'https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?w=400',
                ],
                'short_description': 'Crafted from 100% pure Egyptian organic linen, this dress embodies effortless elegance. The oversized silhouette drapes beautifully, while the natural breathable fabric keeps you comfortable through every season.',
                'composition': ['100% Pure Egyptian Organic Linen', 'Ethically sourced and GOTS certified', 'Natural, undyed fabric — color may vary slightly'],
                'care_instructions': 'Machine wash cold (30°C) on gentle cycle. Do not tumble dry. Iron on medium heat while slightly damp. Dry flat or hang to dry. Do not bleach.',
                'shipping_info': '2-4 business days within Egypt. Free shipping on orders over 500 EGP. 60 EGP flat rate for all other orders.',
                'rating_avg': 4.8,
                'rating_count': 48,
            },
            {
                'title': 'Minimalist Taupe Abaya',
                'category': 'abayas',
                'price': 125.00,
                'original_price': None,
                'badge': 'New',
                'size': 'Free Size',
                'colors': ['Taupe', 'Black', 'Navy'],
                'sizes_available': ['Free Size'],
                'images': ['https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400'],
                'short_description': 'A modern minimalist abaya in our signature taupe tone. Flowing fabric with clean lines for an effortlessly modest look.',
                'composition': ['95% Polyester', '5% Elastane'],
                'care_instructions': 'Hand wash cold. Do not tumble dry. Iron on low heat.',
                'shipping_info': '2-4 business days within Egypt.',
                'rating_avg': 4.6,
                'rating_count': 32,
            },
            {
                'title': 'Cozy Cashmere Knit Top',
                'category': 'casual',
                'price': 75.00,
                'original_price': None,
                'badge': 'Popular',
                'size': 'M / L',
                'colors': ['Cream', 'Camel', 'Dusty Rose'],
                'sizes_available': ['S', 'M', 'L', 'XL'],
                'images': ['https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400'],
                'short_description': 'Ultra-soft cashmere blend knit top for effortless layering.',
                'composition': ['70% Cashmere', '30% Wool'],
                'care_instructions': 'Dry clean only.',
                'shipping_info': '2-4 business days within Egypt.',
                'rating_avg': 4.5,
                'rating_count': 21,
            },
            {
                'title': 'Tailored Organic Linen Blazer',
                'category': 'casual',
                'price': 135.00,
                'original_price': None,
                'badge': '',
                'size': 'S / M / L / XL',
                'colors': ['Natural', 'White', 'Stone'],
                'sizes_available': ['XS', 'S', 'M', 'L', 'XL'],
                'images': ['https://images.unsplash.com/photo-1591085686350-798c0f9faa7f?w=400'],
                'short_description': 'A relaxed tailored blazer in organic linen. The versatile staple for modern wardrobes.',
                'composition': ['100% Organic Linen'],
                'care_instructions': 'Machine wash cold. Hang to dry.',
                'shipping_info': '2-4 business days within Egypt.',
                'rating_avg': 4.7,
                'rating_count': 15,
            },
            {
                'title': 'Pleated A-Line Midi Dress',
                'category': 'sale',
                'price': 65.00,
                'original_price': 95.00,
                'badge': 'Sale -30%',
                'size': 'M / L',
                'colors': ['Dusty Rose', 'Sage', 'Ivory'],
                'sizes_available': ['XS', 'S', 'M', 'L'],
                'images': ['https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=400'],
                'short_description': 'Feminine pleated midi dress with an A-line silhouette. Perfect for any occasion.',
                'composition': ['100% Viscose'],
                'care_instructions': 'Machine wash cold on delicate.',
                'shipping_info': '2-4 business days within Egypt.',
                'rating_avg': 4.3,
                'rating_count': 28,
            },
            {
                'title': 'Classic Egyptian Cotton Shirt',
                'category': 'casual',
                'price': 55.00,
                'original_price': None,
                'badge': 'Essential',
                'size': 'XS / S / M',
                'colors': ['White', 'Blue', 'Stripe'],
                'sizes_available': ['XS', 'S', 'M', 'L'],
                'images': ['https://images.unsplash.com/photo-1598554747436-c9293d6a588f?w=400'],
                'short_description': 'A timeless shirt in premium Egyptian cotton. Crisp, breathable, and effortlessly polished.',
                'composition': ['100% Egyptian Cotton'],
                'care_instructions': 'Machine wash warm. Iron on medium heat.',
                'shipping_info': '2-4 business days within Egypt.',
                'rating_avg': 4.4,
                'rating_count': 19,
            },
        ]

        created_count = 0
        for data in products_data:
            if not Product.objects.filter(title=data['title']).exists():
                product = Product.objects.create(**data)
                created_count += 1

                # Add sample reviews for the first product
                if product.title == 'Oversized Linen Shirt Dress':
                    Review.objects.get_or_create(
                        product=product,
                        reviewer_name='Sarah L.',
                        defaults={
                            'is_verified_buyer': True,
                            'rating': 5,
                            'title': 'Absolutely gorgeous drape and quality!',
                            'body': "The linen quality is unmatched. I've worn this dress three times already and it still looks brand new. The oversized fit is so flattering and the fabric just gets softer with each wash.",
                        }
                    )
                    Review.objects.get_or_create(
                        product=product,
                        reviewer_name='Nour K.',
                        defaults={
                            'is_verified_buyer': True,
                            'rating': 5,
                            'title': 'Perfect summer dress',
                            'body': "I ordered the Cream White and it's even more beautiful in person. The linen is breathable and the cut is universally flattering. Will definitely be ordering more colors!",
                        }
                    )

        self.stdout.write(self.style.SUCCESS(f'[OK] Created {created_count} products'))
        self.stdout.write(self.style.SUCCESS('[OK] Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('-------------------------------------')
        self.stdout.write('BASMAH Backend is ready!')
        self.stdout.write('Admin login: admin@basmah.com / admin123')
        self.stdout.write('Server: python manage.py runserver')
        self.stdout.write('-------------------------------------')
