from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from django import models
from django.contrib.auth import login
from django.urls import reverse
from django.utils import timezone

from grocerysite.forms import Loginform, Registerform
import pdb, sqlite3, hashlib

# from .models import Profile, Order, Product, OrderItem
from grocerysite.models import Product # <- this line is important for search
from .models import Product, OrderItem, Order, UserInfo
from .models import OrderItem


def index(request):
    return render(request, "index.html")

def search(request):
    return render(request, "search.html")

def login(request):
    username = ''
    password = ''

    form = Loginform(request.POST or None)
    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")

      try:
        conn = sqlite3.connect(r"db.sqlite3")
      except Error as e:
        print(e)
      cur = conn.cursor()
      cur.execute("select username, password from auth_user")

      for row in cur:
        if row[0] == username:
          p_hash = hashlib.sha256(password.encode())
          print(p_hash.hexdigest())
          if row[1] == p_hash.hexdigest():
            query = UserInfo.objects.filter(user_name=username.lower())
            result = query[0]
            context={
                    'form': form, 
                    'error': 'The login has been successful', 
                    'username':username,
                    'first_name':result.first_name,
                    'last_name':result.last_name,
                    'address':result.address,
                    'phone_number':result.phone_number
            }
            return render(request, 'user.html', context)

      context={'form': form, 'error': 'The username and password combination is incorrect'}
      return render(request, 'login.html', context)

    context={'form':form, 'error': 'Login'}
    return render(request, "login.html", context)

def register(request):
    form = Registerform(request.POST or None)
    if form.is_valid():
      username = form.cleaned_data.get("username")
      password = form.cleaned_data.get("password")
      address = form.cleaned_data.get("address")
      phone = form.cleaned_data.get("phone")
      p_hash= hashlib.sha256(password.encode())

      try:
        conn = sqlite3.connect(r"db.sqlite3")
      except Error as e:
        print(e)

      cur = conn.cursor()
      cur.execute("select MAX(id) from auth_user")
      for row in cur:
        new_id = row[0] + 1
      cur.execute("insert into auth_user (id, password, last_login, is_superuser, username, last_name, email, is_staff, is_active, date_joined, first_name) values(" + str(new_id) + ",'" + p_hash.hexdigest() + "'," + "NULL,0,'" + username + "','','',1,1,'','');")
      try:
        conn.commit()
      except Error as e:
        print("User already exists")

      with open("grocerysite/data/user_data.csv", "a") as file:
        file.write("\n" + str(new_id) + "," + username + "," + username + "," + username + "," + address + "," + phone)
      context={'form':form, 'error': "Registered in DB"}
      return render(request, 'register.html', context)
      
    context={'form':form, 'error': 'Register'}
    return render(request, 'register.html', context)


def search_result(request):
    search_parameter = request.GET.get('q')
    query1 = Product.objects.filter(product_description__icontains=search_parameter)
    query2 = Product.objects.filter(product_name__icontains=search_parameter)
    results = query1.union(query2)

    context = {'results':results}
    return render(request, "search_result.html", context)


#**********************************************************
def products(request):
    context = {
        'items': Product.objects.all()
    }
    return render(request, "products.html", context)

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_product(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


