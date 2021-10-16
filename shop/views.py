from django.http.response import HttpResponse
from django.shortcuts import render
import datetime
import json
from functools import reduce
from math import ceil
from . import models

# Create your views here.
def index(request, t=3):
    products = models.Product.objects.all()
    final_products = []
    total_cards = t
    print(products)
    product_on_categories =  {"All": []}
    for i in products:
        product_on_categories['All'].append(i)
        if i.category not in product_on_categories:
            product_on_categories[i.category] = []
        if i.sub_category not in product_on_categories:
            product_on_categories[i.sub_category] = []
        product_on_categories[i.category].append(i)
        product_on_categories[i.sub_category].append(i) 
    for x in product_on_categories:
        print(product_on_categories[x])
        finals = []
        no_slides = len(product_on_categories[x]) // total_cards + ceil((len(product_on_categories[x]) / total_cards) - (len(product_on_categories[x]) // total_cards))
        for i in range(no_slides):
            temp = []
            try:
                for z in range(total_cards):
                    temp.append(product_on_categories[x][i*total_cards+z])
            except IndexError:
                pass
            finals.append(temp)
        finals.insert(0, x)
        final_products.append(finals)
    print(final_products)
    for i in final_products:
        print(i)
    return render(request, 'shops/index.html', {"start_product": [products[0], products[1], products[2]], "product": final_products})


def contact(request):
    if (request.method == 'POST'):
        message, name, e_mail = request.POST.get('message', ''), request.POST.get('name', ''), request.POST.get('e-mail', '')
        print(message, name, e_mail, sep='\t')
        contact = models.Contact(message=message, name=name, e_mail=e_mail)
        contact.save()
    return render(request, 'shops/contact.html')

def tracker(request):
    if (request.method == 'GET'):
        return render(request, 'shops/tracker.html', {'found': False, 'searched': False})
    elif (request.method == 'POST'):
        id = request.POST.get('order-id', '')
        email = request.POST.get('e-mail', '')
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
        return render(request, 'shops/checkout.html', {'given_id': id})
    if (request.method == 'POST'):
        items = eval(request.POST.get('inputJSON', ''))
        terms = request.POST.get('terms', '')
        name = request.POST.get('name', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        address = request.POST.get('address', '')
        zip_ = request.POST.get('zip', '')
        e_mail = request.POST.get('e-mail', '')
        if (id != None and e_mail != '' and zip_ != '' and items != '' and terms != '' and name != '' and state != '' and city != '' and address != ''):
            product = models.Product.objects.filter(id=id)
            listItems = {id: {"price": product[0].price, 'qty': 1, 'name': product[0].product_name}, 'date': datetime.datetime.today().strftime('%d %b %m %Y')}
            order = models.Order(array=listItems, price=product[0].price, name=name, state=state, city=city, address=address, zip=zip_, e_mail=e_mail)
            order.save()
            return HttpResponse(f'Thank you for purchasing at "My Awesome Cart". Your order id is: {order.order_id}')
        elif (type(items) == dict and e_mail != '' and zip_ != '' and items != '' and terms != '' and name != '' and state != '' and city != '' and address != ''):
            price = 0
            listItems = {}
            for i in items:
                currItem = models.Product.objects.filter(id=i)[0]
                price += currItem.price * items[i]
                listItems[i] = {"price": currItem.price, "qty": items[i], "name": currItem.product_name}
            listItems['date'] = datetime.datetime.today().strftime('%d %b %m %Y')
            order = models.Order(array=listItems, price=price, name=name, state=state, city=city, address=address, zip=zip_, e_mail=e_mail)
            order.save()
            return HttpResponse(f'Thank you for purchasing at "My Awesome Cart". Your order id is: {order.order_id}')
        else:
            return HttpResponse("An error Occurred while processing your request")
    if (request.method == 'GET' and request.GET.get('checkout', 'False') != 'False'):
        return render(request,'shops/checkout.html')
                
    products = {}
    for i in models.Product.objects.all():
        products[i.id] = [i.product_name, i.price]
    products = json.dumps(products)
    return render(request, 'shops/cart.html', {"products": products})