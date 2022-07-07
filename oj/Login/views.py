from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate

def login_view(request):

    if request.method == 'GET':
        context = {
            'next' : request.GET.get('next')
        }
        return render(request, "login.html", context=context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        next = request.POST.get('next')
        return HttpResponseRedirect(next)
        
    else:
        context = {'error': 'invalid credentials'}
        return render(request, "login.html", context=context)
