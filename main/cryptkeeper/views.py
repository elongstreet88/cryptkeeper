from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import *

def index(request):
    return render(request, 'cryptkeeper/index.html')

@login_required
def transactions(request):
    return render(request, 'cryptkeeper/transactions.html')

@login_required
def hidden(request):
    return HttpResponse("Must be logged in!")