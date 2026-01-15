
import os
import sys
import django
from django.utils.text import slugify

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Product, Category

def fix_slugs():
    print("Fixing category slugs...")
    for category in Category.objects.all():
        original_slug = category.slug
        new_slug = slugify(category.name)
        if original_slug != new_slug:
            print(f"Renaming category slug: '{original_slug}' -> '{new_slug}'")
            category.slug = new_slug
            category.save()

    print("\nFixing product slugs...")
    for product in Product.objects.all():
        original_slug = product.slug
        new_slug = slugify(product.name)
        if original_slug != new_slug:
            print(f"Renaming product slug: '{original_slug}' -> '{new_slug}'")
            product.slug = new_slug
            product.save()

    print("\nDone fixing slugs.")

if __name__ == "__main__":
    fix_slugs()
