from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Count, Max, Min, Avg, Value, Func
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem

# Create your views here.
def say_hello(request):
    # products = Product.objects.values('id', 'title', 'collection__title')
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    #Product.objects.annotate(ordered=Count('orderitem')).order_by('ordered')
    # queryset = Customer.objects.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))

    tagged_item = TaggedItem.objects.get_tags_for(Product, 1)
        
    list(tagged_item)

    orders = False#Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] 
    result = False#Product.objects.aggregate(avg_price=Avg('unit_price'), max_price=Max('unit_price'), min_price=Min('unit_price'))
    queryset = Collection.objects.annotate(products_count=Count('products'))
    list(queryset)
    context =  {
        'name': 'Eman', 
        'orders': orders, 
        'aggregate': result,

        }

    return render(request, 'hello.html',)