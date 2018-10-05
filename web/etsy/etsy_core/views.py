from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'home.html', {})


def login(request):
    if request.method == 'POST':
        previous_page = request.REQUEST.get('next', '')
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(previous_page)
        else:
            
    else:
