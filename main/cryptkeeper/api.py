from rest_framework import routers, serializers, viewsets, status, permissions, generics, mixins
from rest_framework.response import Response
from .models import *
from io import StringIO
from .transaction_parsers import coinbase, blockfi
import json

### Transactions ###

# Serializers define the API representation.
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self,validated_data):
        request = self.context['request']
        transaction = Transaction.objects.create(**validated_data, user = request.user)
        transaction.save()
        return transaction

# ViewSets define the view behavior.
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

### File Importer ###
class TransactionImporterSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file')

class TransactionImporterViewSet(viewsets.ViewSet):
    serializer_class = TransactionImporterSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file.name.startswith("Coinbase"):
            results = coinbase.get_transactions_from_csv(file, user=self.request.user)
        elif file.name.startswith("trade_report_all"):
            results = blockfi.get_transactions_from_csv(file, user=self.request.user)
        return Response(json.dumps(results))