from django.shortcuts import render
# from django import models
from grocerysite.models import Product
from django.contrib.auth import login
from .forms import Loginform
import pdb, sqlite3

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


def search_result(request, search_parameter):
    query1 = Product.objects.filter(product_description__icontains=search_parameter)
    query2 = Product.objects.filter(product_name__icontains=search_parameter)
    results = query1.union(query2)
    print(results.values())

    string_response = str(results.values())
    context = {'results':string_response}
    return render(request, "search_result.html", context)

