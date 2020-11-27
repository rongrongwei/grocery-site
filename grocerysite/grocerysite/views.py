from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
# from django import models
from django.contrib.auth import login
from django.urls import reverse

from .forms import Loginform
import pdb, sqlite3

# from .models import Profile, Order, Product, OrderItem
from grocerysite.models import Product # <- this line is important for search


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
        conn = sqlite3.connect(r"../db.sqlite3")
      except Error as e:
        print(e)
      cur = conn.cursor()
      sql_where = (username,)
      cur.execute("select username from auth_user")
      row = cur.fetchone()
      if row:
        context={'form': form, 'error': 'The login has been successful'}
        return render(request, 'login.html', context)
      else:
        context={'form': form, 'error': 'The username and password combination is incorrect'}
        return render(request, 'login.html', context)

    context={'form':form, 'error': 'Test'}
    return render(request, "login.html", context)


def search_result(request):
    search_parameter = request.GET.get('q')
    query1 = Product.objects.filter(product_description__icontains=search_parameter)
    query2 = Product.objects.filter(product_name__icontains=search_parameter)
    results = query1.union(query2)

    context = {'results':results}
    return render(request, "search_result.html", context)


@login_required()
def add_to_cart(request, **kwargs):
    #grab usr profile
    user_profile = get_object_or_404(Profile, user=request.user)
    #filter prducts by id
    product = Product.objects.filter(id=kwargs.get('item_id' ,"")).first()
    #create orderitem of the selected grocery
    order_item, status = OrderItem.objects.get_or_create(product=product)
    return redirect(reverse('products:product-list'))








