from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Count, Max, Min, Avg
from store.models import Product, OrderItem, Order

# Create your views here.
def say_hello(request):
    # products = Product.objects.values('id', 'title', 'collection__title')
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] 

    result = Product.objects.aggregate(avg_price=Avg('unit_price'), max_price=Max('unit_price'), min_price=Min('unit_price'))

    return render(request, 'hello.html', {'name': 'Eman', 'orders': orders, 'aggregate': result})