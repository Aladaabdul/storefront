from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Product, ProductImage
from .models import Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from .serializers import ProductSerializer, ReviewSerializer, CustomerSerializer, OrderSerializer, CreateOrderSerializer, ProductImageSerializer
from .serializers import CollectionSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, UpdateOrderSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly
 
# Create your views here.

class ProductViewSet(ModelViewSet):
       queryset = Product.objects.all()
       serializer_class = ProductSerializer
       filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
       filterset_class = ProductFilter
       pagination_class = DefaultPagination
       permission_classes = [IsAdminOrReadOnly]
       search_fields = ['title']
       ordering_fields = ['unit_price', 'last_update']
        

class CollectionViewSet(ModelViewSet):
       queryset = Collection.objects.all()
       serializer_class = CollectionSerializer
       permission_classes = [IsAdminOrReadOnly]
       filter_backends = [OrderingFilter]
       ordering_fields = ['title', 'id']

class ReviewViewSet(ModelViewSet):
       queryset = Review.objects.all()
       serializer_class = ReviewSerializer

# it won't support GET request
class CartViewSet(CreateModelMixin, 
                  GenericViewSet, 
                  DestroyModelMixin, 
                  RetrieveModelMixin):
       queryset = Cart.objects.prefetch_related('items__product').all()
       serializer_class = CartSerializer


class CartItemViewset(ModelViewSet):
       # Prevent put request in our class
       http_method_names = ['get', 'patch', 'post', 'delete']
       
       def get_serializer_class(self):
              if self.request.method == 'POST':
                     return AddCartItemSerializer
              if self.request.method == 'PATCH':
                     return UpdateCartItemSerializer
              return CartItemSerializer
       
       def get_serializer_context(self):
              return {'cart_id': self.kwargs['cart_pk']}

       # Filter item by Cart id
       def get_queryset(self):
              return CartItem.objects \
                     .filter(cart_id= self.kwargs['cart_pk']) \
                     .select_related('product') # Implement Eager loading to avoid selecting similar queries for reading the product


class CustomerViewSet(ModelViewSet):
       queryset = Customer.objects.all()
       serializer_class = CustomerSerializer
       permission_classes = [IsAdminOrReadOnly]

       # # Set permission for different Method
       # def get_permissions(self):
       #        if self.request.method == "GET":
       #               return [AllowAny()]
       #        return [IsAuthenticated()]
              

       # Create a customize action
       @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated]) # Action will be availiable on the list view i.e store/customer/me
       def me(self, request):
              customer = Customer.objects.get(user_id = request.user.id)
              if request.method == 'GET':
                     serializer = CustomerSerializer(customer)
                     return Response(serializer.data)
              elif request.method == 'PUT':
                     serializer = CustomerSerializer(customer, data=request.data)
                     serializer.is_valid(raise_exception=True)
                     serializer.save()
                     return Response(serializer.data)
              
class  OrderViewset(ModelViewSet):
       queryset = Order.objects.all()
       http_method_names = ['get', 'post', 'patch', 'delete', 'option', 'head']

       def get_permissions(self):
              if self.request.method in ["PATCH", "DELETE"]:
                     return [IsAdminUser()]
              return [IsAuthenticated()]

       def create(self, request, *args, **kwargs):
              serializer = CreateOrderSerializer(
                     data=request.data,
                     context={'user_id': self.request.user.id})
              serializer.is_valid(raise_exception=True)
              order = serializer.save()
              serializer = OrderSerializer(order)
              return Response(serializer.data)
       
       def get_serializer_class(self):
              if self.request.method == 'POST':
                     return CreateOrderSerializer
              if self.request.method == 'PATCH':
                     return UpdateOrderSerializer
              return OrderSerializer

class ProductImageViewSet(ModelViewSet):
       serializer_class = ProductImageSerializer

       def get_serializer_context(self):
              product_pk = self.kwargs.get('product_pk') or self.kwargs.get('pk')
              return {'product_id': product_pk}
              # return {'product_id': self.kwargs['product_id']}

       def get_queryset(self):
              product_pk = self.kwargs.get('product_pk') or self.kwargs.get('pk')
              return ProductImage.objects.filter(product_id=product_pk)