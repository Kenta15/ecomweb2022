from email.message import EmailMessage
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cartData, guestOrder,countryData
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm,EditUserInfo
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
# Create your views here.

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}
    return render(request,'store/store.html',context)

def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'items':items, 'order':order, 'cartItems':cartItems,'country':country}
    return render(request,'store/cart.html',context)


def checkout(request):

    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.user.is_authenticated:
        name = request.user.username
        customer = Customer.objects.get(name=name)
        shipping_address = customer.address
    else:
        shipping_address = ""

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'items':items, 'order':order, 'cartItems':cartItems,'country':country,'shipping_address':shipping_address}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity-1
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    transaciton_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer, order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaciton_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        if not request.user.is_authenticated:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment is complete',safe=False)

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = request.POST.get('username')
            email = request.POST.get('email')
            customer = Customer.objects.create(user=user,name=username,email=email,country='United States')
            login(request,user)
            mydict = {'username': username}
            subject = 'Welcome to our website'
            message = get_template('email.html').render(mydict)
            from_email = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail = EmailMessage(subject,message,from_email,recipient)
            send_mail.content_subtype = 'html'
            send_mail.send()
            return redirect('store')

    context = {'form': form}
    return render(request,'account/register.html',context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            messages.info(request, 'Login Failed')

    return render(request,'account/login.html')

def forgotPage(request):
    return render(request,'account/forgot.html')

def logoutPage(request):
    logout(request)
    return redirect('login')

def countryPage(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'cartItems':cartItems,'country':country}
    return render(request,'account/country.html',context)

def updateCountry(request):
    data = json.loads(request.body)
    selected_country = data['selected_country']

    name = request.user.username
    user = Customer.objects.get(name=name)
    user.country = selected_country
    user.save()

    return JsonResponse('Country was changed',safe=False)

def settingPage(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.user.is_authenticated:
        form = EditUserInfo(instance=request.user)
        if request.method == 'POST':
            form = EditUserInfo(request.POST,instance=request.user)
            name = request.user.username
            if form.is_valid():
                user = Customer.objects.get(name=name)
                user.name = request.POST.get('username')
                user.email = request.POST.get('email')
                user.save()
                form.save()
                messages.success(request,'User info has been successfully updated')
    else:
        form = EditUserInfo()

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)
            
    context={'cartItems':cartItems,'country':country,'form':form}
    return render(request,'account/settings.html',context)

def grocery(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/grocery.html',context)

def cosmetic(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/cosmetic.html',context)

def gaming(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/gaming.html',context)

def electronic(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/electronic.html',context)

def apparel(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/apparel.html',context)

def book(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/book.html',context)

def daily(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/daily.html',context)

def kitchen(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/kitchen.html',context)

def pet(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/pet.html',context)

def health(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/category/health.html',context)

def bestseller(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    array = []
    
    for count in range(1,100):
        for product in products:
            if product.rank == count:
                array.append(product)

    context={'array':array, 'cartItems':cartItems,'country':country}

    return render(request,'store/bestseller.html',context)

def contactPage(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'cartItems':cartItems,'country':country}
    return render(request,'account/contact.html',context)

def newPage(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)

    context={'products':products, 'cartItems':cartItems,'country':country}

    return render(request,'store/new.html',context)

def searchPage(request):

    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    country_data = countryData(request)
    country = country_data['country']

    if request.method == 'POST':
        product_list = []
        search = request.POST.get('search').lower()
        for product in products:
            lower_product = product.name.lower()
            if search in lower_product:
                product_list.append(product)
        context={'product_list':product_list, 'cartItems':cartItems,'country':country}
        return render(request,'store/search.html',context)