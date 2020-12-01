from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from django.contrib import messages
from .forms import Loginform
import pdb, sqlite3
from .models import Product, OrderItem, Order


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

##---------- CART Views ---------------------------------------------
@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('products:product-list'))
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('products:product-list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('shopping_cart:order_summary'))




