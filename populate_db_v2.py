
import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Category, Product

# Define Categories and Products
data = {
    'Electronics': [
        ('Smartphone X', 999.00), 
        ('Laptop Pro', 1299.00),
        ('Wireless Earbuds', 199.00),
        ('4K Smart TV', 799.00),
        ('Digital Camera', 549.00),
        ('Gaming Console', 499.00),
    ],
    'Clothing': [
        ('Denim Jacket', 89.00),
        ('Summer Floral Dress', 59.00),
        ('Running Sneakers', 120.00),
        ('Cotton Basic T-Shirt', 25.00),
        ('Slim Fit Jeans', 65.00),
        ('Hoodie Essentials', 45.00),
    ],
    'Home & Living': [
        ('Automatic Coffee Maker', 150.00),
        ('Memory Foam Pillow', 40.00),
        ('Modern Desk Lamp', 35.00),
        ('Ceramic Flower Vase', 22.00),
        ('Wall Art Frame', 55.00),
    ],
    'Sports & Outdoors': [
        ('Yoga Mat Premium', 30.00),
        ('Dumbbell Set 10kg', 75.00),
        ('Tennis Racket', 110.00),
        ('Hiking Backpack', 95.00),
        ('Stainless Water Bottle', 18.00),
    ],
    'Beauty & Health': [
        ('Luxury Perfume', 85.00),
        ('Anti-Aging Cream', 60.00),
        ('Hair Dryer Pro', 120.00),
        ('Makeup Brush Set', 45.00),
        ('Organic Face Wash', 20.00),
    ]
}

# Image mapping (simplified to use what we definitely have)
# We downloaded: hero_1.jpg, women.jpg, children.jpg, men.jpg, cloth_1.jpg, shoe_1.jpg, cloth_2.jpg, cloth_3.jpg
img_pool = ['hero_1.jpg', 'women.jpg', 'children.jpg', 'men.jpg', 'cloth_1.jpg', 'shoe_1.jpg', 'cloth_2.jpg', 'cloth_3.jpg']
static_img_dir = os.path.join(os.getcwd(), 'shop', 'static', 'images')

def populate():
    print("Populating database...")
    import random
    
    for cat_name, products in data.items():
        slug = cat_name.lower().replace(' & ', '-').replace(' ', '-')
        category, _ = Category.objects.get_or_create(name=cat_name, slug=slug)
        print(f"Category: {category.name}")
        
        for prod_name, price in products:
            prod_slug = prod_name.lower().replace(' ', '-')
            product, created = Product.objects.get_or_create(
                slug=prod_slug,
                defaults={
                    'name': prod_name,
                    'category': category,
                    'price': price,
                    'description': f'Description for {prod_name}.',
                    'available': True
                }
            )
            
            if created:
                # Assign a random image from our pool
                img_file = random.choice(img_pool)
                img_path = os.path.join(static_img_dir, img_file)
                if os.path.exists(img_path):
                    with open(img_path, 'rb') as f:
                        product.image.save(img_file, File(f), save=True)
                print(f" - Created: {prod_name}")
            else:
                 print(f" - Exists: {prod_name}")

if __name__ == '__main__':
    populate()
