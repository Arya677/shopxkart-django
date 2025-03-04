from django.shortcuts import get_object_or_404, render
from carts.views import _cart_id
from carts.models import CartItem
from .models import Product
from category.models import Category
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def store(request, category_slug=None): # Define a function to handle the store
    categories = None
    products =None

    if category_slug != None: # If the category_slug is not None
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category = categories, is_available=True)
        paginator = Paginator(products, 6) # Show 6 products per page
        page = request.GET.get('page') # Get the current page number
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') # Get all products
        paginator = Paginator(products, 6) # Show 6 products per page
        page = request.GET.get('page') # Get the current page number
        paged_products = paginator.get_page(page) # Get the products for the current page
        product_count = products.count() # Get the total number of products

    context = {
        'products': paged_products, # Pass the products to the template
        'product_count': product_count, # Pass the product count to the template
    } 
    return render(request,'store.html',context) # Return the render request

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }         
    return render(request, 'product_detail.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
        product_count = products.count()
    else:
        products = Product.objects.none()
        product_count = 0
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)
