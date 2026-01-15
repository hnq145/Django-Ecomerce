
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Product, Category

try:
    c_count = Category.objects.count()
    p_count = Product.objects.count()
    
    with open('db_status.txt', 'w') as f:
        f.write(f"Categories: {c_count}\n")
        f.write(f"Products: {p_count}\n")
        # List a few to be sure
        for p in Product.objects.all()[:5]:
             f.write(f"- {p.name}\n")

except Exception as e:
    with open('db_status.txt', 'w') as f:
        f.write(f"Error: {e}\n")
