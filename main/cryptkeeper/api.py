from django.db.models.aggregates import Count
from django.db.models.fields import FloatField
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
import json
from django.db.models import Sum, Q, F
from django.db.models.functions import Coalesce, Abs
from django.core import serializers as django_serializer
from django.http import JsonResponse
from .core.cryptkeeper import tools as cryptkeeper_tools
from .core.crypto_price_finder import crypto_price_finder
from .models import *


#
# Transactions
# 
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ['user']

    def create(self,validated_data):
        request = self.context['request']
        transaction = Transaction.objects.create(**validated_data, user = request.user)
        transaction.save()
        return transaction

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

#
# File Importer
#
class TransactionImporterSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file')

class TransactionImporterViewSet(viewsets.ViewSet):
    serializer_class = TransactionImporterSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        file        = request.FILES.get('file')
        file_name   = file.name

        results = cryptkeeper_tools.import_transactions_from_file(
            file_name       = file_name, 
            in_memory_file  = file, 
            user            = self.request.user
        )

        return Response(json.dumps(results))

#
# Spot Price
#
class SpotPriceSerializer(serializers.Serializer):
    asset_symbol = serializers.CharField()
    datetime     = serializers.DateTimeField(format="%Y-%m-%d-%H:%M:%S")

class SpotPriceViewSet(viewsets.ViewSet):
    serializer_class = SpotPriceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        return Response([])

    #ex: http://localhost:8000/api/spot-price/btc/2020-04-30-15-15-30/
    @action(methods=['get'], detail=True, url_path='(?P<datetime>[^/.]+)', serializer_class= SpotPriceSerializer())
    def get_spot_price(self, request, datetime, pk=None):
        serializer = SpotPriceSerializer(data={'asset_symbol': pk, 'datetime': datetime})
        serializer.is_valid(raise_exception=True)

        price_info = crypto_price_finder.get_usd_price(
            target_time     = serializer.validated_data["datetime"],
            asset_symbol    = serializer.validated_data["asset_symbol"]
        )

        if not price_info["success"]:
            return Response("Request could not be completed.", status=400)
        
        return Response(price_info)

#
# Asset Info
# 
class AssetInfoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        asset_transactions = Transaction.objects                                                                                     \
            .filter(user=request.user)                                                                                               \
            .values("asset_symbol")                                                                                                  \
            .annotate(total_asset_quantity             = Sum("asset_quantity"))                                                      \
            .annotate(total_asset_quantity_buy         = Sum("asset_quantity"           , filter=Q(transaction_type="Buy")))         \
            .annotate(total_asset_quantity_sell        = Sum("asset_quantity"           , filter=Q(transaction_type="Sell")))        \
            .annotate(total_asset_quantity_interest    = Sum("asset_quantity"           , filter=Q(transaction_type="Interest")))    \
            .annotate(total_asset_quantity_airdrop     = Sum("asset_quantity"           , filter=Q(transaction_type="Airdrop")))     \
            .annotate(total_usd_buy                    = Sum("usd_total_with_fees"      , filter=Q(transaction_type="Buy")))         \
            .annotate(total_usd_sell                   = Sum("usd_total_with_fees"      , filter=Q(transaction_type="Sell")))        \
            .annotate(total_transacted_usd             = Sum("usd_total_with_fees"))                                                 \
            .annotate(total_transactions               = Count("usd_total_with_fees"))                                               \
            .annotate(average_price_buy                = Abs(F("total_usd_buy") / F("total_asset_quantity_buy")))

        data = list(asset_transactions)
        return Response(data)

    #ex: http://localhost:8000/api/asset-info/btc/
    def retrieve(self, request, pk=None):
        return Response([])