from django.urls import path

from . import views

from rest_framework import routers, serializers, viewsets
from .models import *

# Serializers define the API representation.
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['user']

# ViewSets define the view behavior.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=self.request.user)

urlpatterns = [
    path('', views.index, name='index'),
    path('hidden', views.hidden, name='hidden'),
    path('transactions', views.transactions, name='transactions'),
]
