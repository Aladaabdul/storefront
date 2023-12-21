from rest_framework import serializers
from django.db import transaction
from .signals import order_created
from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     product_id = self.context.get('product_id')
    #     return ProductImage.objects.create(product_id=product_id, **validated_data)

    def create(self, validated_data):
        product_id = self.context.get('product_id')

        try:
            product = Product.objects.get(pk=product_id)
        except Exception:
            raise serializers.ValidationError("Product does not exist")
        
        product_image = ProductImage(product=product, **validated_data)
        product_image.save()
        return product_image


    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id','title','unit_price','price_with_tax', 'images']
        

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title','id','featured_product']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review 
        fields = ['id', 'date', 'name', 'description', 'product']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    # Set Total_price
    total_price = serializers.SerializerMethodField()

    #Define a method for total_price
    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    # Declare id as readonly (only to be read from the server)
    id = serializers.UUIDField(read_only=True)
    # Items as readonly (From database)
    items = CartItemSerializer(many=True, read_only = True)

    #Set Total_price for cart
    total_price = serializers.SerializerMethodField()

    #Define a Total_price method
    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

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

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership' ]

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given id found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is Empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():

            cart_id=self.validated_data['cart_id']

            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects\
                    .select_related('product')\
                    .filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                order=order,
                product=item.product,
                unit_price=item.product.unit_price,
                quantity=item.quantity
            )for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            
            order_created.send_robust(self.__class__, order=order)

            return 
            