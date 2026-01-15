
import os
import random
import django
from django.core.files import File
from django.core.files import File
import urllib.request

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Category, Product

# 1. Setup Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)

# 2. Define Data
# "Chém bừa" - Diverse categories and products
DATA = {
    'Electronics': [
        ('Smartphone Galaxy Ultra', 1199.99),
        ('Laptop Probook 15', 899.50),
        ('Wireless Noise Cancelling Headphones', 249.99),
        ('Smart Watch Series 7', 399.00),
        ('4K Monitor 27 inch', 349.00),
        ('Bluetooth Speaker Mini', 49.99),
        ('Gaming Mouse RGB', 59.99),
        ('Mechanical Keyboard', 89.99),
        ('External SSD 1TB', 129.99),
        ('Webcam HD 1080p', 69.99),
    ],
    'Fashion & Clothing': [
        ('Men\'s Cotton T-Shirt', 19.99),
        ('Women\'s Summer Dress', 39.99),
        ('Classic Blue Jeans', 49.50),
        ('Leather Jacket', 129.00),
        ('Running Sneakers', 89.99),
        ('Hoodie Streetwear', 55.00),
        ('Formal Shirt White', 35.00),
        ('Baseball Cap', 15.00),
        ('Winter Scarf', 25.00),
        ('Ankle Boots', 79.99),
    ],
    'Home & Kitchen': [
        ('Coffee Maker Automatic', 79.99),
        ('Blender High Speed', 49.99),
        ('Non-stick Frying Pan', 29.99),
        ('Chef Knife Set', 59.99),
        ('Organic Cotton Bed Sheets', 69.00),
        ('Memory Foam Pillow', 35.00),
        ('Desk Lamp LED', 25.99),
        ('Ceramic Vase', 19.99),
        ('Wall Clock Vintage', 22.50),
        ('Scented Candles Set', 18.00),
    ],
    'Books & Literature': [
        ('The Great Adventure', 14.99),
        ('Python Programming Guide', 45.00),
        ('History of the World', 29.99),
        ('Modern Cooking Recipes', 24.50),
        ('Sci-Fi Galaxy Wars', 12.99),
        ('Self-Improvement 101', 16.00),
        ('Mystery in the Manor', 11.99),
    ],
    'Sports & Outdoors': [
        ('Yoga Mat Anti-slip', 25.00),
        ('Dumbbell Set 20kg', 89.99),
        ('Camping Tent 4-Person', 149.99),
        ('Hiking Backpack Waterproof', 59.99),
        ('Tennis Racket Pro', 120.00),
        ('Basketball Indoor', 29.99),
        ('Football Standard', 24.99),
        ('Cycling Helmet', 45.00),
    ],
    'Beauty & Health': [
        ('Facial Moisturizer', 22.00),
        ('Vitamin C Serum', 18.50),
        ('Hair Dryer Professional', 55.00),
        ('Electric Toothbrush', 39.99),
        ('Sunscreen SPF 50', 15.00),
        ('Makeup Kit Complete', 59.99),
        ('Perfume Elegance', 75.00),
    ],
    'Toys & Games': [
        ('Building Blocks Set', 39.99),
        ('Remote Control Car', 49.99),
        ('Board Game Family Fun', 29.99),
        ('Puzzle 1000 Pieces', 19.99),
        ('Plush Teddy Bear', 24.99),
        ('Action Figure Hero', 15.99),
    ]
}

import tempfile

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
    
    # Optional: Clear existing data? 
    # User said "Chém bừa lên cũng được" imply just adding stuff is fine, 
    # but cleaning up might be cleaner if they want a fresh start.
    # Let's keep existing and just add new ones to be safe, or get_or_create.
    
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
                # Download and save image
                # We group downloads to save time/bandwidth, maybe reuse a few images?
                # For "diversity", let's try to get a unique one for each, or at least one per category.
                # To be faster, let's use the category name for the image text.
                
                temp_path = download_placeholder_image(cat_name)
                if temp_path:
                    # Construct a filename
                    file_name = f"{prod_slug}.png"
                    try:
                        with open(temp_path, 'rb') as f:
                            product.image.save(file_name, File(f), save=True)
                    except Exception as e:
                        print(f"Error saving image for {prod_name}: {e}")
                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
            else:
                print(f" - Product exists: {prod_name}")

    print("Population complete!")

if __name__ == '__main__':
    populate()
