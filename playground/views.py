from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem, Order

# Create your views here.
def say_hello(request):
    # products = Product.objects.values('id', 'title', 'collection__title')
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    products = OrderItem.objects.select_related('order__customer', 'product').order_by('-order__id')
        
    return render(request, 'hello.html', {'name': 'Eman', 'products': products})