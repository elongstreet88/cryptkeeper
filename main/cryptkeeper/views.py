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
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TransactionForm()
        form.user = User
    
    return render(request, 'cryptkeeper/transactions.html', {'form': TransactionForm})

@login_required
def hidden(request):
    return HttpResponse("Must be logged in!")