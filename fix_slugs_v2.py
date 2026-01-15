
import os
import sys
import django
from django.utils.text import slugify

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from shop.models import Product, Category

def fix_data():
    print("Starting slug fix...")
    
    # Fix Categories
    for cat in Category.objects.all():
        try:
            old_slug = cat.slug
            # Ensure strictly valid characters: letters, numbers, underscores, hyphens
            new_slug = slugify(cat.name)
            if old_slug != new_slug:
                print(f"Fixing Category {cat.id}: {old_slug} -> {new_slug}")
                cat.slug = new_slug
                cat.save()
        except Exception as e:
            print(f"Error fixing category {cat.name}: {e}")

    # Fix Products
    for p in Product.objects.all():
        try:
            old_slug = p.slug
            new_slug = slugify(p.name)
            
            # Use a fallback if slugify returns empty (unlikely for proper names)
            if not new_slug:
                new_slug = f"product-{p.id}"
                
            if old_slug != new_slug:
                print(f"Fixing Product {p.id}: {old_slug} -> {new_slug}")
                p.slug = new_slug
                p.save()
            elif "'" in old_slug: # Explicit check for apostrophes if slugify didn't catch it for some reason?
                 # Django slugify REMOVES apostrophes. 
                 # So if we are here, slugify(p.name) returned something with apostrophe? NO.
                 # It implies old_slug == new_slug (which shouldn't happen if old has ' and new doesn't).
                 pass

        except Exception as e:
            print(f"Error fixing product {p.name}: {e}")

    print("Finished slug fix.")

if __name__ == '__main__':
    fix_data()
