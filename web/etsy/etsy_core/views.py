from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'home.html', {})

def shop(request, shop_id):
    return render(request, '', {})

def create_shop(request):
    return render(request, '', {})

def products(request, shop_id):
    if request.method == 'GET':
        #Get all products of a shop
    else if request.method == 'POST':
        #Create a new product of that shop
    return render(request, '', {})
