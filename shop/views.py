from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import datetime
import json
from math import ceil
from . import models

# Create your views here.
def index(request, t=3):
    products = models.Product.objects.all()
    product_on_categories =  {"All": []}
    for i in products:
        product_on_categories['All'].append(i)
        if i.category not in product_on_categories:
            product_on_categories[i.category] = []
        if i.sub_category not in product_on_categories:
            product_on_categories[i.sub_category] = []
        product_on_categories[i.category].append(i)
        product_on_categories[i.sub_category].append(i) 
    return render(request, 'shops/index.html', {"product": products})


def contact(request):
    if (request.method == 'POST'):
        message, name, e_mail = request.POST.get('message', ''), request.POST.get('name', ''), request.POST.get('e-mail', '')
        if (message == '' or name == '' or e_mail == ''):
            return render(request, 'shops/contact.html', {'missing': True})
        print(message, name, e_mail, sep='\t')
        contact = models.Contact(message=message, name=name, e_mail=e_mail)
        contact.save()
    return render(request, 'shops/contact.html')

def tracker(request):
    if (request.method == 'GET'):
        if (not request.user.is_authenticated):
            return redirect('/shop/sign-up')
        return render(request, 'shops/tracker.html', {'found': False, 'searched': False})
    elif (request.method == 'POST'):
        id = request.POST.get('order-id', '')
        email = request.user.email
        findId = models.Order.objects.filter(order_id=id)
        if (len(findId) == 0):
            return render(request, 'shops/tracker.html', {'found': False, 'searched': True})
        elif (findId[0].e_mail == email):
            x = datetime.datetime.today() - datetime.datetime.strptime(findId[0].array['date'], '%d %b %m %Y')
            reachingDate = datetime.datetime.strptime(findId[0].array['date'], '%d %b %m %Y') + datetime.timedelta(days=3, hours=12)
            dateReaching = 'Reached 'if x.days > 3 else 'In transit'
            return render(request, 'shops/tracker.html', {'found': True, 'searched': True, 'product': findId[0], 'status': dateReaching, 'arrival': reachingDate})
        else:
            return render(request, 'shops/tracker.html', {'found': False, 'searched': True})
    

def search(request):
    return HttpResponse('We are at Search')

def productview(request, id):
    product = models.Product.objects.filter(id=id)
    print(product[0])
    return render(request, 'shops/product.html', {'product': product[0]})

def cart(request, id=None):
    if (id != None and request.method == 'GET' and len(models.Product.objects.filter(id=id)) != 0):
        if (not request.user.is_authenticated):
            return redirect('/shop/sign-up')
        return render(request, 'shops/checkout.html', {'given_id': id})
    if (request.method == 'POST'):
        items = eval(request.POST.get('inputJSON', ''))
        terms = request.POST.get('terms', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        address = request.POST.get('address', '')
        zip_ = request.POST.get('zip', '')
        print(request.user.username, request.user.email)
        if (id != None and zip_ != '' and items != '' and terms != '' and state != '' and city != '' and address != ''):
            product = models.Product.objects.filter(id=id)
            listItems = {id: {"price": product[0].price, 'qty': 1, 'name': product[0].product_name}, 'date': datetime.datetime.today().strftime('%d %b %m %Y')}
            order = models.Order(array=listItems, price=product[0].price, name=request.user.username, state=state, city=city, address=address, zip=zip_, e_mail=request.user.email)
            order.save()
            return redirect('/shop/my-items?scroll=True')

        elif (type(items) == dict and zip_ != '' and items != '' and terms != '' and state != '' and city != '' and address != ''):
            price = 0
            listItems = {}
            for i in items:
                currItem = models.Product.objects.filter(id=i)[0]
                price += currItem.price * items[i]
                listItems[i] = {"price": currItem.price, "qty": items[i], "name": currItem.product_name}
            listItems['date'] = datetime.datetime.today().strftime('%d %b %m %Y')
            order = models.Order(array=listItems, price=price, name=request.user.username, state=state, city=city, address=address, zip=zip_, e_mail=request.user.email)
            order.save()
            return redirect('/shop/my-items?scroll=True')
        else:
            return HttpResponse("An error Occurred while processing your request")
    if (request.method == 'GET' and request.GET.get('checkout', 'False') != 'False'):
        if (not request.user.is_authenticated):
            return redirect('/shop/sign-up')
        return render(request,'shops/checkout.html')
                
    products = {}
    for i in models.Product.objects.all():
        products[i.id] = [i.product_name, i.price]
    products = json.dumps(products)
    return render(request, 'shops/cart.html', {"products": products})


def sign_up(request):
    if (request.method == 'POST'):
        email = request.POST.get('e-mail')
        password = request.POST.get('password')
        username = request.POST.get('username')
        age = request.POST.get('age')
        mobile = request.POST.get('mobile')

        if (email != None and password != None and username != None and age != None and mobile != None and len(User.objects.filter(email=email)) == 0 and age.isnumeric() and int(age) >= 13 and mobile.isnumeric() and len(mobile) == 10 and len(User.objects.filter(username=username)) == 0):
            print(age, mobile)
            print(username, password, email)

            # creating the user

            user = User.objects.create_user(username, email.lower(), password)
            user.save()

            person = models.OtherUserDetails(email=email.lower(), age=int(age), mobile=mobile)
            person.save()

            login(request, user)

            return redirect('/shop')

        else:
            return render(request, 'shops/signUp.html', {"invalid": True})

    return render(request, 'shops/signUp.html')

def log_in(request):
    if (request.method == 'POST'):
        email = request.POST.get('e-mail')
        password = request.POST.get('password')
        user = None
        try:
            user:User = User.objects.get(email=email.lower())
        except:
            pass
        if (user is not None):
            user = user if user.check_password(password) else None

        if (user is not None):
            login(request, user)
            print('User logged in')
            return redirect('/shop')

        return HttpResponse('Error')
    return render(request, 'shops/log-in.html')

def log_out(request):
    logout(request)
    print('Logged out user')
    return redirect('/shop')

def my_account(request):
    if (request.user.is_authenticated):
        all_items = models.Order.objects.filter(e_mail=request.user.email)
        print(User.objects.get(username=request.user.username))
        remaining_details = models.OtherUserDetails.objects.filter(email=request.user.email)
        print(remaining_details)
        total_price = 0
        for i in all_items:
            total_price += i.price
        return render(request, 'shops/my_account.html', {"remaining_details": remaining_details[0], "total_orders": len(all_items), "total_price": total_price, "awesome_points": (total_price // len(all_items)) if len(all_items) != 0 else 0, "awesome_cash_value": ((total_price // len(all_items)) // 2) if len(all_items) != 0 else 0})
    return redirect('/shop/')

def my_items(request):
    if (request.user.is_authenticated):
        scroll = request.GET.get('scroll')
        print(scroll)
        if scroll != None:
            scroll = True
        else:
            scroll = False
        orders_by_user = models.Order.objects.filter(e_mail=request.user.email)
        orders_by_user_json = [[i.array[x] for x in i.array] for i in orders_by_user]
        for i in range(len(orders_by_user)):
            orders_by_user_json[i].append(orders_by_user[i].order_id)
        return render(request, 'shops/my_items.html', {"orders": orders_by_user_json, "length_orders": len(orders_by_user), "scroll": scroll})
    return HttpResponse('404 Page not found error')


def edit_profile(request):
    if (request.user.is_authenticated):
        if (request.method == 'POST'):
            passFirst = request.POST.get('passFirst', None)
            if request.user.check_password(passFirst):
                return render(request, 'shops/edit-profile.html', {'password_first': False})
            elif (request.user.check_password(passFirst) is False and passFirst is not None):
                return render(request, 'shops/edit-profile.html', {'password_first': True, "invalid": True})
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')
                mobile_number = request.POST.get('mobile')
                e_mail = request.POST.get('e-mail')
                if (username != '' or password != '' or mobile_number != '' or e_mail != ''):
                    user = User.objects.get(username=request.user.username)
                    other_user_details = models.OtherUserDetails.objects.get(email=request.user.email)
                    all_orders = models.Order.objects.filter(e_mail=request.user.email)

                    user.email=e_mail if e_mail != '' else request.user.email
                    user.username=username if username != '' else request.user.username
                    if password != '':
                        user.set_password(password)
                    user.save()
                    login(request, user)
                    other_user_details.mobile=mobile_number if mobile_number != '' else other_user_details.mobile
                    other_user_details.email=e_mail if e_mail != '' else request.user.email

                    other_user_details.save()

                    for i in all_orders:
                        i.name = request.user.username
                        i.e_mail = request.user.email
                        i.save()
    
                    return redirect('/shop/my-account')
                else:
                    return render(request, 'shops/edit-profile.html', {"password_first": True, 'invalid': True})
            
        return render(request, 'shops/edit-profile.html', {"password_first": True})
    else:
        return HttpResponse('404 page not found')