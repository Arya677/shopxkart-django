from django.shortcuts import render
from store.models import Product

def index(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    return render(request,'index.html',context)

def register(request):
    return render(request,'register.html')

def signin(request):
    return render(request,'login.html')

def product_detail(request):        
    return render(request, 'product_detail.html')