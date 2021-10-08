from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def index(request):
    return render(request, 'cryptkeeper/index.html')

@login_required
def hidden(request):
    return HttpResponse("Must be logged in!")