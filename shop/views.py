from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Product, OrderItem, Home, CATEGORY_CHOICES, Order
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template import loader
import stripe
import random
import string
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY



def index(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    product_objects = Product.objects.filter(active='Active')
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name, active='Active') or product_objects.filter(category__icontains=item_name,active='Active') or product_objects.filter(color__icontains=item_name,active='Active')
    if request.GET.get('sort-low'):
        product_objects = Product.objects.filter(active='Active').order_by('price')
    if request.GET.get('sort-high'):
        product_objects = Product.objects.filter(active='Active').order_by('-price')
    if request.GET.get('Tees'):
        product_objects = Product.objects.filter(category='Tees',active='Active')
    if request.GET.get('Accessories'):
        product_objects = Product.objects.filter(category='Accessories',active='Active')
    if request.GET.get('Outerwear'):
        product_objects = Product.objects.filter(category='Outerwear',active='Active')
    if request.GET.get('Shirts'):
        product_objects = Product.objects.filter(category='Shirts',active='Active')
    if request.GET.get('Sweatshirts'):
        product_objects = Product.objects.filter(category='Sweatshirts',active='Active')
    if request.GET.get('Jackets'):
        product_objects = Product.objects.filter(category='Jackets',active='Active')
    if request.GET.get('Shoes'):
        product_objects = Product.objects.filter(category='Shoes',active='Active')
    if request.GET.get('Bottoms'):
        product_objects = Product.objects.filter(category='Bottoms',active='Active')
    if request.GET.get('Sale'):
        product_objects = Product.objects.filter(sale='On Sale',active='Active')
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    return render(request,'shop/index.html',{'product_objects': product_objects, 'cart':cart, 'cartqty':cartqty})

def detail(request,id):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    product_object = Product.objects.get(id=id)
    category = product_object.category
    return render(request,'shop/detail.html', {'product_object':product_object, 'cart':cart, 'cartqty':cartqty, 'category':category})

def cart(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    qty = request.GET.get("qty")
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    subtotal = 0
    for orderitem in cart:
        subtotal += orderitem.item_total
    tax = float(subtotal)*.0725
    taxval = "{:.2f}".format(tax)
    shipping = cartqty*2
    shippingval = "{:.2f}".format(shipping)
    total = float(subtotal)+float(tax)+float(shipping)
    totalval = "{:.2f}".format(total)
    return render(request,'shop/cart.html', {'cart':cart, 'cartqty':cartqty, 'subtotal':subtotal, 'taxval':taxval, 'shippingval':shippingval, 'totalval':totalval})

def checkout(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    qty = request.GET.get("qty")
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    subtotal = 0
    for orderitem in cart:
        subtotal += orderitem.item_total
    tax = float(subtotal)*.0725
    taxval = "{:.2f}".format(tax)
    shipping = cartqty*2
    shippingval = "{:.2f}".format(shipping)
    total = float(subtotal)+float(tax)+float(shipping)
    totalval = "{:.2f}".format(total)
    return render(request,'shop/checkout.html', {'cart':cart, 'cartqty':cartqty, 'subtotal':subtotal, 'taxval':taxval, 'shippingval':shippingval, 'totalval':totalval})

def home(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    qty = request.GET.get("qty")
    images = Home.objects.all()
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    return render(request,'shop/home.html', {'cart':cart, 'cartqty':cartqty,'images':images})


def add_to_cart(request,id):
    request.session.set_expiry(2000)
    product = get_object_or_404(Product, id=id)
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    qty = int(request.GET.get("qty"))
    size = request.GET.get("size")
    if not OrderItem.objects.filter(product__id=product.id, size=size, slug=the_id).exists() and size:
        order_item = OrderItem.objects.create(product=product)
        order_item.slug = the_id
        order_item.quantity = qty
        order_item.image_link = product.id
        order_item.size = size
        order_item.category = product.category
        order_item.sale = product.sale
        if order_item.sale=="On Sale":
            order_item.price = product.discount_price
            order_item.item_total = product.discount_price*qty
        else:
            order_item.price = product.price
            order_item.item_total = product.price*qty
        order_item.image_1 = product.image_1
        order_item.save()
    elif OrderItem.objects.filter(product__id=product.id, size=size, slug=the_id).exists() and size:
        order_item = OrderItem.objects.get(product=id, size=size,slug=request.session['order_slug'])
        order_item.quantity += qty
        order_item.item_total += product.price*qty
        order_item.save()
    else:
        pass
    return redirect(product)

def remove_from_cart(request,id):
    orderitem = OrderItem.objects.get(id=id)
    OrderItem.objects.filter(id=id).delete()
    return redirect(cart)


def update_quantity(request,id):
    quantity = int(request.GET.get("quantity"))
    orderitem = OrderItem.objects.get(id=id)
    price = orderitem.price
    orderitem.item_total = orderitem.price*quantity 
    OrderItem.objects.filter(id=id).update(item_total=quantity*price)
    OrderItem.objects.filter(id=id).update(quantity=quantity) 
    return redirect(cart)

def charge(request):
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    qty = request.GET.get("qty")
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    subtotal = 0
    for orderitem in cart:
        subtotal += orderitem.item_total
    tax = float(subtotal)*.0725
    taxval = "{:.2f}".format(tax)
    shipping = cartqty*2
    shippingval = "{:.2f}".format(shipping)
    total = float(subtotal)+float(tax)+float(shipping)
    totalval = "{:.2f}".format(total)
    totalcharge = round(total*100)
    amount = totalcharge
    receipt_email=request.POST['billemail']
    request.session['phone'] = request.POST.get('phone')
    request.session['billemail'] = request.POST.get('billemail')
    request.session['shipaddress'] = request.POST.get('shipaddress1')+" "+request.POST.get('shipaddress2') +" "+ request.POST.get('shipcity') +", "+ request.POST.get('shipstate') +" "+ request.POST.get('shipzip')

    customer = stripe.Customer.create(
        email=request.POST['billemail'],
        name=request.POST['billfirstname'] + ' ' + request.POST['billlastname'],
        source=request.POST['stripeToken']
    )

    stripe.Charge.create(
    customer=customer,
    amount=totalcharge,
    currency="usd",
    receipt_email=request.POST['billemail'],
    description="Test Charge",
    )

    subject = 'Order Confirmation'
    message = 'Order is in! Thank you!'
    html_message = loader.render_to_string('shop/order.html', {'cart':cart, 'cartqty':cartqty, 'subtotal':subtotal, 'taxval':taxval, 'shippingval':shippingval, 'totalval':totalval})
    from_email = settings.EMAIL_HOST_USER
    to_list = receipt_email
    send_mail(subject,message,from_email,[to_list],html_message=html_message,fail_silently=True)
    return redirect(orderconfirmation)


def orderconfirmation(request):
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    subtotal = 0
    for orderitem in cart:
        subtotal += orderitem.item_total
    tax = float(subtotal)*.0725
    taxval = "{:.2f}".format(tax)
    shipping = cartqty*2
    shippingval = "{:.2f}".format(shipping)
    total = float(subtotal)+float(tax)+float(shipping)
    totalval = "{:.2f}".format(total)
    totalcharge = round(total*100)
    ordernumber = random_string_generator()
    order = Order.objects.create(
        order_number = ordernumber,
        shipping_address = request.session['shipaddress'],
        phone_number = request.session['phone'],
        email = request.session['billemail'],
        subtotal = subtotal,
        tax = taxval,
        shipping_cost = shippingval,
        total = totalval,
    )
    for orderitem in cart:
        order.order_item_list.add(orderitem.id)
    randomstring = random_string_generator()
    request.session['order_slug'] = randomstring
    the_id = randomstring
    return render(request,'shop/orderconfirmation.html', {'cart':cart, 'cartqty':cartqty, 'subtotal':subtotal, 'taxval':taxval, 'shippingval':shippingval, 'totalval':totalval, 'ordernumber':ordernumber})

def random_string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def champion(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    product_objects = Product.objects.filter(title__icontains="reverse weave",active="Active")
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = Product.objects.filter(title__icontains=item_name,active="Active") or Product.objects.filter(category__icontains=item_name,active="Active") or Product.objects.filter(color__icontains=item_name,active="Active")
    if request.GET.get('sort-low'):
        product_objects = Product.objects.filter(active="Active").order_by('price')
    if request.GET.get('sort-high'):
        product_objects = Product.objects.filter(active="Active").order_by('-price')
    if request.GET.get('Tees'):
        product_objects = Product.objects.filter(category='Tees',active="Active")
    if request.GET.get('Accessories'):
        product_objects = Product.objects.filter(category='Accessories',active="Active")
    if request.GET.get('Outerwear'):
        product_objects = Product.objects.filter(category='Outerwear',active="Active")
    if request.GET.get('Shirts'):
        product_objects = Product.objects.filter(category='Shirts',active="Active")
    if request.GET.get('Sweatshirts'):
        product_objects = Product.objects.filter(category='Sweatshirts',active="Active")
    if request.GET.get('Jackets'):
        product_objects = Product.objects.filter(category='Jackets',active="Active")
    if request.GET.get('Shoes'):
        product_objects = Product.objects.filter(category='Shoes',active="Active")
    if request.GET.get('Bottoms'):
        product_objects = Product.objects.filter(category='Bottoms',active="Active")
    if request.GET.get('Sale'):
        product_objects = Product.objects.filter(sale='On Sale',active="Active")
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    return render(request,'shop/index.html',{'product_objects': product_objects, 'cart':cart, 'cartqty':cartqty})


def yeezy(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    product_objects = Product.objects.filter(title__icontains="yeezy",active="Active")
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = Product.objects.filter(title__icontains=item_name,active="Active") or Product.objects.filter(category__icontains=item_name,active="Active") or Product.objects.filter(color__icontains=item_name,active="Active")
    if request.GET.get('sort-low'):
        product_objects = Product.objects.filter(active="Active").order_by('price')
    if request.GET.get('sort-high'):
        product_objects = Product.objects.filter(active="Active").order_by('-price')
    if request.GET.get('Tees'):
        product_objects = Product.objects.filter(category='Tees',active="Active")
    if request.GET.get('Accessories'):
        product_objects = Product.objects.filter(category='Accessories',active="Active")
    if request.GET.get('Outerwear'):
        product_objects = Product.objects.filter(category='Outerwear',active="Active")
    if request.GET.get('Shirts'):
        product_objects = Product.objects.filter(category='Shirts',active="Active")
    if request.GET.get('Sweatshirts'):
        product_objects = Product.objects.filter(category='Sweatshirts',active="Active")
    if request.GET.get('Jackets'):
        product_objects = Product.objects.filter(category='Jackets',active="Active")
    if request.GET.get('Shoes'):
        product_objects = Product.objects.filter(category='Shoes',active="Active")
    if request.GET.get('Bottoms'):
        product_objects = Product.objects.filter(category='Bottoms',active="Active")
    if request.GET.get('Sale'):
        product_objects = Product.objects.filter(sale='On Sale',active="Active")
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    return render(request,'shop/index.html',{'product_objects': product_objects, 'cart':cart, 'cartqty':cartqty})

def offwhite(request):
    try:
        the_id = request.session['order_slug']
    except:
        randomstring = random_string_generator()
        request.session['order_slug'] = randomstring
        the_id = randomstring
    product_objects = Product.objects.filter(title__icontains="off-white",active="Active")
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = Product.objects.filter(title__icontains=item_name,active="Active") or Product.objects.filter(category__icontains=item_name,active="Active") or Product.objects.filter(color__icontains=item_name,active="Active")
    if request.GET.get('sort-low'):
        product_objects = Product.objects.filter(active="Active").order_by('price')
    if request.GET.get('sort-high'):
        product_objects = Product.objects.filter(active="Active").order_by('-price')
    if request.GET.get('Tees'):
        product_objects = Product.objects.filter(category='Tees',active="Active")
    if request.GET.get('Accessories'):
        product_objects = Product.objects.filter(category='Accessories',active="Active")
    if request.GET.get('Outerwear'):
        product_objects = Product.objects.filter(category='Outerwear',active="Active")
    if request.GET.get('Shirts'):
        product_objects = Product.objects.filter(category='Shirts',active="Active")
    if request.GET.get('Sweatshirts'):
        product_objects = Product.objects.filter(category='Sweatshirts',active="Active")
    if request.GET.get('Jackets'):
        product_objects = Product.objects.filter(category='Jackets',active="Active")
    if request.GET.get('Shoes'):
        product_objects = Product.objects.filter(category='Shoes',active="Active")
    if request.GET.get('Bottoms'):
        product_objects = Product.objects.filter(category='Bottoms',active="Active")
    if request.GET.get('Sale'):
        product_objects = Product.objects.filter(sale='On Sale',active="Active")
    cart = OrderItem.objects.filter(slug=request.session['order_slug'])
    cartqty = 0
    for orderitem in cart:
        cartqty += orderitem.quantity
    return render(request,'shop/index.html',{'product_objects': product_objects, 'cart':cart, 'cartqty':cartqty})