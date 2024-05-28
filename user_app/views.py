from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render

from admin_app.models import Table, Menu
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from user_app.models import Customers, Cart

# Create your views here.
from django.http import JsonResponse


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        table = Table.authenticate(username=username, password=password)
        if table is not None:
            request.session['username'] = username
            request.session['password'] = password
            request.session['table'] = table.id

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})

    return render(request, 'user/login.html')


def home(request):
    try:
        table_id = request.session['table']
        is_active = Table.objects.filter(id=table_id).first().is_active
        menu = Menu.objects.all()
        return render(request, 'user/home.html', {'is_active': is_active,
                                                  'menu': menu, 'table_id': table_id})
    except:
        return render(request, 'user/login.html')


def add_customer(request):
    if request.method == 'POST':

        name = request.POST['name']
        mobile = request.POST['mobile']
        table_id = request.session['table']

        if name and mobile:
            Customers.objects.create(name=name, mobile=mobile, table_id=table_id)
            Table.objects.filter(id=table_id).update(is_active=True)

    return HttpResponse("success")
    return render(request, 'user/home.html')


# def cart(request):
#     is_active = request.user.is_active
#     return render(request, 'user/cart.html', {'is_active': is_active})

def add_to_cart(request):
    print(request.method, 'kk')
    if request.method == 'POST':
        print('jj')
        item_id = request.POST.get('item_id')
        table_id = request.POST.get('table_id')
        # Assuming you have a method to get the item from the database
        item = Menu.objects.get(pk=item_id)
        table = Table.objects.filter(id=table_id).first()
        cart_item = Cart.objects.create(
            table=table,  # Assuming you have a way to get the table
            menu=item,
            quantity=1,  # Assuming default quantity is 1
            total_price=item.price,  # Assuming total price is the same as item price
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def cart(request):
    table_id = request.session.get('table')
    is_active = Table.objects.filter(id=table_id).first().is_active
    if not table_id:
        return render(request, 'user/cart.html', {'is_active': is_active, 'cart_items': []})

    table = Table.objects.filter(id=table_id).first()
    if not table:
        return render(request, 'user/cart.html', {'is_active': is_active, 'cart_items': []})

    cart_items = Cart.objects.filter(table=table)
    total_amount = sum(item.total_price * item.quantity for item in cart_items)
    return render(request, 'user/cart.html', {'is_active': is_active,
                                              'cart_items': cart_items, 'total':total_amount})


def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def increase_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)
    if cart_item.quantity == 1:
        cart_item.delete()
        return redirect('cart')

    cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart')