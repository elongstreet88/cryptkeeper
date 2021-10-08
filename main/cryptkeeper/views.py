from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

@login_required
def hidden(request):
    return HttpResponse("Must be logged in!")