from django.conf import settings
from shop.models import Product

class Wishlist(object):
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = []
        self.wishlist = wishlist

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist.append(product_id)
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.wishlist:
            self.wishlist.remove(product_id)
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.wishlist
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            yield product

    def __len__(self):
        return len(self.wishlist)
    
    def clear(self):
        del self.session[settings.WISHLIST_SESSION_ID]
        self.save()
