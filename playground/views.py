from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from store.models import Product, OrderItem

# Create your views here.
def say_hello(request):
    products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    return render(request, 'hello.html', {'name': 'Eman', 'products': products})