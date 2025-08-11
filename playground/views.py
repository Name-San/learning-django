from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F, Count, Max, Min, Avg, Value, Func
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem
from templated_mail.mail import BaseEmailMessage

# Create your views here.
def say_hello(request):
    # products = Product.objects.values('id', 'title', 'collection__title')
    # products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    #Product.objects.annotate(ordered=Count('orderitem')).order_by('ordered')
    # queryset = Customer.objects.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))

    # tagged_item = TaggedItem.objects.get_tags_for(Product, 1)
        
    # list(tagged_item)

    # orders = False#Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5] 
    # result = False#Product.objects.aggregate(avg_price=Avg('unit_price'), max_price=Max('unit_price'), min_price=Min('unit_price'))
    # queryset = Collection.objects.annotate(products_count=Count('products'))
    # list(queryset)
    # context =  {
    #     'name': 'Eman', 
    #     'orders': orders, 
    #     'aggregate': result,

    #     }

    try:
        # mail_admins('Sample Subject', 'This is a sample messaage', html_message='Click this link to redirect in <a href="google.com">google</a>')
        # message = EmailMessage('subject', 'message', 'info@ecommerce.com', ['john@ecommerce.com'])
        # message.attach_file('playground/static/images/django.png')
        # message.send()
        message = BaseEmailMessage(
            template_name='emails/hello.html',
            context={'name': 'Eman'}
        )
        message.attach_file('playground/static/images/django.png')
        message.send(['eman@ecommerce.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html')