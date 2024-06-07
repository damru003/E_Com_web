from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from django.views import View
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


# Create your views here.

def index(request):
    print ('you are =', request.session.get('email'))
    return render (request, 'index.html')

class products(View):
    
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1 
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart [product] = 1

        request.session['cart'] = cart
        print ('cart', request.session['cart'])
        return redirect ('products')
    
    
    def get(self, request):


        cart = request.session.get('cart')
        if not cart:
            request.session.cart = {}



        products = None
        categories = Category.get_all_categories()
        categoryid = request.GET.get('category')
        if categoryid:
            products = Product.get_all_products_by_category_id(categoryid)
        else:
            products = Product.get_all_products()
    
        context = {
        'products': products,
        'categories':categories
        }
        return render (request, 'products.html', context)
    
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        value = {
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        
        #Validation
        error_message = None
        
        if(not first_name):
            error_message = "First Name Required !!"
        elif len(first_name) < 4:
            error_message = 'First name must be 4 Character long or more'
        elif not last_name:
            error_message = "Last Name Required !!"
        elif len(last_name) < 4:
            error_message = 'Last name must be 4 Character long or more'
        elif not phone:
            error_message = 'Phone Number required !!'
        elif len(phone) < 10:
            error_message = "Phone number must be 10 Character long"
        elif not email:
            error_message = "Email Required"
        elif not password:
            error_message = "Password must be Required !!"
        elif len(password) < 6:
            error_message = "Password must be 8 character long"
        
        #Error_messages 
        
        if  not  error_message:
            
            customer = Customer(first_name=first_name,last_name=last_name,phone=phone,email=email,password=password)
            customer.password = make_password(customer.password)
            customer.save()
            
            return redirect('index')
            
            
        else:
            data = {
                'error':error_message,
                'values': value
            }
            return render (request, 'signup.html',data)
        
    return render (request, 'signup.html')

class Login(View):
    return_url = ''

    def get(self,request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    def post(self,request):
        email  = request.POST.get('email')
        password = request.POST.get('password')
        
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer :
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                     Login.return_url = None
                     return redirect('index')
            else:
                error_message = "Email or Password Invalid"
        else:
            error_message = "Email or Password Invalid"
        print(email,password)
        
        error = {
            'error' : error_message
        }
        
        return render (request, 'login.html', error)
    
def logout(request):
    request.session.clear()
    return redirect ('login')

class Cart(View):
    
    def get(self,request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids) 
        print (products)

        context = {
            'products':products
        }
        return render (request, 'cart.html', context)
    
class Checkout(View):
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))

        print (address,phone,customer,cart,products)

        for product in products:
            order = Order(customer=Customer(id=customer), 
                          product=product,
                          price=product.price,
                          quantity=cart.get(str(product.id)),
                          address=address,
                          phone=phone)
            
            order.placeorder()
        request.session['cart'] = {}
            
        return redirect ('cart')
    
class Orders(View):

    @method_decorator(auth_middleware)
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)

        context = {
            'orders':orders
        }
        print(orders)
        return render (request, 'order.html',context)