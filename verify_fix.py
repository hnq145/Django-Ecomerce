import os
import sys
import django

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

try:
    django.setup()
    from shop.models import Product
    print("SUCCESS: Model imported successfully")
except Exception as e:
    print(f"ERROR: {e}")
