from django.shortcuts import render
# from django import models
from grocerysite.models import Product
import pdb

def index(request):
    return render(request, "index.html")

def search(request):
    return render(request, "search.html")

def login(request):
    return render(request, "login.html")

def search_result(request, search_parameter):
    query1 = Product.objects.filter(product_description__icontains=search_parameter)
    query2 = Product.objects.filter(product_name__icontains=search_parameter)
    results = query1.union(query2)
    print(results.values())

    string_response = str(results.values())
    context = {'results':string_response}
    return render(request, "search_result.html", context)

