
import os
import random
import django
from django.core.files import File
import urllib.request
import tempfile
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Category, Product

# 1. Setup Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

DATA = {
    'Electronics': [
        ('Smartphone Galaxy Ultra', 1199.99),
        ('Laptop Probook 15', 899.50),
        ('Wireless Noise Cancelling Headphones', 249.99),
        ('Smart Watch Series 7', 399.00),
        ('4K Monitor 27 inch', 349.00),
    ],
    'Fashion': [
        ('Men\'s Cotton T-Shirt', 19.99),
        ('Women\'s Summer Dress', 39.99),
        ('Classic Blue Jeans', 49.50),
        ('Leather Jacket', 129.00),
        ('Running Sneakers', 89.99),
    ],
    'Home': [
        ('Coffee Maker Automatic', 79.99),
        ('Blender High Speed', 49.99),
        ('Non-stick Frying Pan', 29.99),
        ('Chef Knife Set', 59.99),
        ('Organic Cotton Bed Sheets', 69.00),
    ],
    'Health': [
        ('Facial Moisturizer', 22.00),
        ('Vitamin C Serum', 18.50),
        ('Hair Dryer Professional', 55.00),
        ('Electric Toothbrush', 39.99),
        ('Sunscreen SPF 50', 15.00),
    ]
}

def download_placeholder_image(text):
    """Downloads a placeholder image and returns the temp file path."""
    url = f"https://dummyimage.com/600x400/cccccc/000000.png&text={text.replace(' ', '+')}"
    
    try:
        print(f"Downloading image for {text} from {url}...")
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        # Create a temp file manually to avoid Windows file lock/permission issues with NamedTemporaryFile
        fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(fd) # Close the low-level file descriptor immediately
        
        with urllib.request.urlopen(req) as response:
            with open(temp_path, 'wb') as f:
                f.write(response.read())
        return temp_path
    except Exception as e:
        print(f"Failed to download image: {e}")
        return None

def populate():
    print("Starting database population...")
    
    for cat_name, products in DATA.items():
        slug = cat_name.lower().replace(' & ', '-').replace(' ', '-')
        category, created = Category.objects.get_or_create(name=cat_name, slug=slug)
        if created:
            print(f"Created Category: {cat_name}")
        else:
            print(f"Category exists: {cat_name}")

        for prod_name, price in products:
            prod_slug = prod_name.lower().replace(' ', '-')
            product, created = Product.objects.get_or_create(
                slug=prod_slug,
                defaults={
                    'name': prod_name,
                    'category': category,
                    'price': price,
                    'description': f"This is a fantastic {prod_name}. It features high quality materials and excellent craftsmanship. Perfect for your needs!",
                    'available': True
                }
            )

            if created:
                print(f" - Created Product: {prod_name}")
                temp_path = download_placeholder_image(cat_name)
                if temp_path:
                    file_name = f"{prod_slug}.png"
                    try:
                        with open(temp_path, 'rb') as f:
                            product.image.save(file_name, File(f), save=True)
                    except Exception as e:
                        print(f"Error saving image for {prod_name}: {e}")
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
            else:
                print(f" - Product exists: {prod_name}")

    print("Population complete!")

if __name__ == '__main__':
    populate()
