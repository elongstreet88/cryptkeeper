from rest_framework import routers, serializers, viewsets
from rest_framework import permissions
from .models import *

# Serializers define the API representation.
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self,validated_data):
        request = self.context['request']
        user = request.user
        transaction = Transaction.objects.create(value=validated_data['value'])
        transaction.user = user
        point.save()
        return transaction

# ViewSets define the view behavior.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=self.request.user)
