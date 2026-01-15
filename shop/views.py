from django.shortcuts import render, get_object_or_404
from cart.forms import CartAddProductForm
from .models import Category, Product

# from django.views import generic

# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    # Price Filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
        
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created')
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)


# class ProductListView(generic.ListView):
#     template_name = 'shop/product/list.html'

#     def get_queryset(self):
#         return Product.objects.filter(available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = None
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
#         context['categories'] = Category.objects.all()





from .forms import ReviewForm

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    
    # Reviews
    reviews = product.reviews.filter(active=True)
    new_review = None
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
    else:
        review_form = ReviewForm()
        
    # Related Products
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]

    # Recently Viewed Products Logic
    recent_products = request.session.get('recent_products', [])
    # Ensure current product is at the start of the list
    if id in recent_products:
        recent_products.remove(id)
    recent_products.insert(0, id)
    # Limit to 5
    if len(recent_products) > 5:
        recent_products = recent_products[:5]
    request.session['recent_products'] = recent_products
    
    # Fetch objects (excluding current)
    # To preserve order, we might need to sort them in Python, but for simplicity:
    viewed_products_ids = [pid for pid in recent_products if pid != id]
    viewed_products = Product.objects.filter(id__in=viewed_products_ids, available=True)
    
    # Sort them by the order in the session list
    viewed_products = sorted(viewed_products, key=lambda p: viewed_products_ids.index(p.id)) if viewed_products else []

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'new_review': new_review,
        'review_form': review_form,
        'related_products': related_products,
        'viewed_products': viewed_products
    }
    return render(request, 'shop/product/detail.html', context)


# class ProductDetialView(generic.DetailView):

#     template_name = 'shop/product/detail.html'
#     model = Product
#     form_class = CartAddProductForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = get_object_or_404(Product, 
#         id=id, slug=slug, available=True)
#         return context