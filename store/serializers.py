from decimal import Decimal
from rest_framework import serializers
from .models import Cart, CartItem, Product, Collection, Review

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

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']   

    def get_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id','items', 'total_price']
        read_only_fields = ['id', 'items', 'total_price']    

    def get_total_price(self, cart: Cart):
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())