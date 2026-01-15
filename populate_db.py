
import os
import django
import random
import shutil
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Category, Product

# Define Categories and Products
data = {
    'Electronics': [
        ('Smartphone X', 999.00, 'men.jpg'), 
        ('Laptop Pro', 1299.00, 'hero_1.jpg'),
        ('Wireless Earbuds', 199.00, 'cloth_1.jpg'), # Placeholder mapping
        ('4K Smart TV', 799.00, 'hero_1.jpg'),
        ('Digital Camera', 549.00, 'cloth_2.jpg'),
        ('Gaming Console', 499.00, 'men.jpg'),
    ],
    'Clothing': [
        ('Denim Jacket', 89.00, 'men.jpg'),
        ('Summer Floral Dress', 59.00, 'women.jpg'),
        ('Running Sneakers', 120.00, 'shoe_1.jpg'),
        ('Cotton Basic T-Shirt', 25.00, 'cloth_1.jpg'),
        ('Slim Fit Jeans', 65.00, 'cloth_2.jpg'),
        ('Hoodie Essentials', 45.00, 'cloth_3.jpg'),
    ],
    'Home & Living': [
        ('Automatic Coffee Maker', 150.00, 'cloth_2.jpg'),
        ('Memory Foam Pillow', 40.00, 'cloth_3.jpg'),
        ('Modern Desk Lamp', 35.00, 'shoe_1.jpg'),
        ('Ceramic Flower Vase', 22.00, 'hero_1.jpg'),
        ('Wall Art Frame', 55.00, 'women.jpg'),
    ],
    'Sports & Outdoors': [
        ('Yoga Mat Premium', 30.00, 'cloth_3.jpg'),
        ('Dumbbell Set 10kg', 75.00, 'shoe_1.jpg'),
        ('Tennis Racket', 110.00, 'men.jpg'),
        ('Hiking Backpack', 95.00, 'hero_1.jpg'),
        ('Stainless Water Bottle', 18.00, 'cloth_1.jpg'),
    ],
    'Beauty & Health': [
        ('Luxury Perfume', 85.00, 'women.jpg'),
        ('Anti-Aging Cream', 60.00, 'cloth_2.jpg'),
        ('Hair Dryer Pro', 120.00, 'hero_1.jpg'),
        ('Makeup Brush Set', 45.00, 'cloth_1.jpg'),
        ('Organic Face Wash', 20.00, 'children.jpg'),
    ]
}

# Path to static images we downloaded earlier
static_img_dir = os.path.join(os.getcwd(), 'shop', 'static', 'images')

def populate():
    print("Populating database with diverse products...")
    
    for cat_name, products in data.items():
        # Create Category
        slug = cat_name.lower().replace(' & ', '-').replace(' ', '-')
        category, created = Category.objects.get_or_create(name=cat_name, slug=slug)
        if created:
            print(f"Created Category: {cat_name}")
        
        for prod_name, price, img_file in products:
            # Create Product
            prod_slug = prod_name.lower().replace(' ', '-')
            product, p_created = Product.objects.get_or_create(
                slug=prod_slug,
                defaults={
                    'name': prod_name,
                    'category': category,
                    'price': price,
                    'description': f'This is a high-quality {prod_name}. Suitable for all your needs. Best in class performance and durability.',
                    'available': True
                }
            )
            
            if p_created:
                # Assign Image
                img_path = os.path.join(static_img_dir, img_file)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        product.image.save(img_file, File(f), save=True)
                print(f"  - Added Product: {prod_name}")
            else:
                print(f"  - Skipped (Exists): {prod_name}")

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
