
import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Category, Product

DATA = {
    'Electronics': [('Smartphone', 1000)],
    'Clothing': [('T-Shirt', 20)]
}

print("Starting population...")
with open('population_log.txt', 'w') as f:
    f.write("Starting...\n")
    for cat_name, products in DATA.items():
        cat, _ = Category.objects.get_or_create(name=cat_name, slug=cat_name.lower())
        f.write(f"Category: {cat_name}\n")
        for p_name, price in products:
            Product.objects.get_or_create(name=p_name, category=cat, slug=p_name.lower(), price=price)
            f.write(f"Product: {p_name}\n")
    f.write("Done.\n")
print("Done")
