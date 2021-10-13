from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('transactions', views.transactions, name='transactions'),
    path('hidden', views.hidden, name='hidden'),
]
