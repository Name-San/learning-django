from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']  

    def create(self, validated_data):
        return Review.objects.create(product_id=self.context['product_id'], **validated_data)

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'unit_price', 'price_with_tax', 'inventory', 'collection', 'last_update']    

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax', read_only=True)

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity
    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
    
class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        product_id = self.validated_data.get('product_id')
        quantity = self.validated_data.get('quantity')
        cart_id = self.context.get('cart_id')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id','items', 'total_price']
        read_only_fields = ['id', 'items', 'total_price']    

    def get_total_price(self, cart: Cart):
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()

    class Meta:
        model = OrderItem
        fields =  ['product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'payment_status', 'placed_at', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cartId = serializers.UUIDField()

    def save(self, **kwargs):
        (customer, created) = Customer.objects.get_or_create(user_id=self.context.get('user_id'))
        Order.objects.create(customer=customer)