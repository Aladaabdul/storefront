from django.conf import settings
from django.contrib import admin
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator
from uuid import uuid4
from .validators import validate_file_size

class Promotion(models.Model):
     discription = models.CharField(max_length=255)
     discount = models.FloatField()

     

class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null= True, related_name='+') # Many To One Field Relationship
    
    def __str__(self) -> str:
         return self.title

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=225)
    slug = models.SlugField()
    description = models.TextField(null= True, blank= True)
    unit_price = models.DecimalField(
         max_digits=6, 
         decimal_places=2,
         validators=[MinValueValidator(1)])
    inventory = models.IntegerField(
         validators=[MinValueValidator(1)]
    )
    last_update = models.DateField(auto_now_add=True)
    models.ForeignKey(Collection, on_delete=models.PROTECT,)
    promotion = models.ManyToManyField(Promotion, blank= True)

    def __str__ (self) -> str:
         return self.title
    
    class Meta:
         ordering = ['title']

class ProductImage(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
     image = models.ImageField(upload_to='store/images',
                               validators=[validate_file_size])

class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_SILVER = "S"
    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold" ),
    ]
    # delete first_name
    # delete last_name
    # delete email 
    # They are all in the User model 
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=50, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    def __str__(self):
         return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name') # Allow use to by name in Admin page
    def first_name(self):
         return self.user.first_name
    
    @admin.display(ordering="user__last_name")
    def last_name(self):
         return self.user.last_name
    
    class Meta:
         ordering = ['user__first_name', 'user__last_name']

class Order(models.Model):
        PAYMENT_STATUS_PENDING = "P"
        PAYMENT_STATUS_COMPLETE = "C"
        PAYMENT_STATUS_FAILED = "F"

        PAYMENT_STATUS_CHIOCE = [
            (PAYMENT_STATUS_PENDING, "P"),
            (PAYMENT_STATUS_COMPLETE, "C"),
            (PAYMENT_STATUS_FAILED, "F"),

        ]

        placed_at = models.DateField(auto_now_add=True)
        payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHIOCE, default=PAYMENT_STATUS_PENDING)
        customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

        class Meta:
             permissions = [
                  ('cancel_order', 'can_cancel_order')
             ]


class OrderItem(models.Model):
     order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
     product = models.ForeignKey(Product, on_delete=models.PROTECT)
     quality = models.PositiveSmallIntegerField()
     unit_price = models.DecimalField(max_digits=6 , decimal_places=2)
     
class Address(models.Model):
     street = models.CharField(max_length=255)
     city = models.CharField(max_length=255)
     customer = models.ForeignKey(Customer,on_delete= models.PROTECT)
    

class Cart(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid4)
     created_at = models.DateField(auto_now_add=True)

class CartItem(models.Model):
     cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name='items') #Instead  of Cartitem_set
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.PositiveSmallIntegerField()

     #Unique Constrait
     #Avoid creating duplicate record
     class Meta:
          unique_together = [['cart', 'product']]

class Review(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
     name = models.CharField(max_length=255)
     description = models.TextField()
     date = models.DateField(auto_now_add=True)

