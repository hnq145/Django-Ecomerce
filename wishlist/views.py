from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .wishlist import Wishlist
from django.contrib import messages

def wishlist_add(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.add(product=product)
    messages.success(request, f'Added {product.name} to wishlist!')
    return redirect('wishlist:wishlist_detail')

def wishlist_remove(request, product_id):
    wishlist = Wishlist(request)
    product = get_object_or_404(Product, id=product_id)
    wishlist.remove(product)
    return redirect('wishlist:wishlist_detail')

def wishlist_detail(request):
    wishlist = Wishlist(request)
    return render(request, 'wishlist/detail.html', {'wishlist': wishlist})
