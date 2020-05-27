from django.db import models
from django.conf import settings
from multiselectfield import MultiSelectField
from django.shortcuts import reverse
from django.urls import reverse_lazy

# Create your models here.
CATEGORY_CHOICES = (
    ('Accessories','Accessories'),
    ('Outerwear','Outerwear'),
    ('Tees','Tees'),
    ('Shirts','Shirts'),
    ('Sweatshirts','Sweatshirts'),
    ('Jackets','Jackets'),
    ('Shoes','Shoes'),
    ('Bottoms','Bottoms'),    
)

SALE_CHOICES = (
    ('Not On Sale','Not On Sale'),
    ('On Sale','On Sale'), 
)
ACTIVE_CHOICES = (
    ('Active','Active'),
    ('Sold Out','Sold Out'), 
)

SIZE_CHOICES = (
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('2XL','2XL'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
    ('13','13'),
    ('One Size', 'One Size')
)

ORDER_STATUS_CHOICES = (
    ('Not Started','Not Started'),
    ('Shipped','Shipped'),
    ('Issues','Issues'),
    ('Refunded','Refunded'),
)


class Home(models.Model):
    main_image = models.CharField(max_length=300)
    image_1 = models.CharField(max_length=300)
    image_2 = models.CharField(max_length=300)
    image_3 = models.CharField(max_length=300)
    image_4 = models.CharField(max_length=300)
    image_5 = models.CharField(max_length=300)


class Product(models.Model):
    category_choices = CATEGORY_CHOICES
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image_1 = models.CharField(max_length=300)
    image_2 = models.CharField(max_length=300)
    image_3 = models.CharField(max_length=300)
    image_4 = models.CharField(max_length=300)
    image_5 = models.CharField(max_length=300)
    size = MultiSelectField(choices=SIZE_CHOICES,
                                 max_choices=6,
                                 max_length=100)
    color = models.CharField(max_length=200)
    sale = models.CharField(max_length=20, choices=SALE_CHOICES, default="Not On Sale")
    active = models.CharField(max_length=20, choices=ACTIVE_CHOICES, default="Active")
    
    def __str__(self):
        return self.title

    def get_price(self):
        return self.price

    def get_description(self):
        return self.description
    
    def get_image(self):
        return self.image_1

    def get_size(self):
        return self.size

    def get_absolute_url(self):
        return reverse('detail', kwargs={
            'id': self.id
        })
    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'id': self.id
        })



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    size = models.CharField(max_length=100, default="none")
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES, default="Blank=True")
    price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    item_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    image_1 = models.CharField(max_length=300, default="") 
    slug = models.CharField(max_length=6, default="")
    image_link = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.quantity} of size {self.size} of {self.product.title} in {self.product.color}"
    
    def get_absolute_url(self):
        return reverse('cart', kwargs={
            'id': self.id
        })

    def get_remove_from_cart_url(self):
        return reverse('remove-from-cart', kwargs={
            'id': self.id
        })


class Order(models.Model):
    order_number = models.CharField(max_length=6, default="")
    order_item_list = models.ManyToManyField(OrderItem, blank=True, null=True, default="")
    shipping_address = models.CharField(max_length=300, default="") 
    phone_number = models.CharField(max_length=20, default="")
    email = models.CharField(max_length=300, default="") 
    subtotal = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    tracking = models.CharField(max_length=300, default="") 
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES, default="Not Started")
    def __str__(self):
        return self.order_number


    