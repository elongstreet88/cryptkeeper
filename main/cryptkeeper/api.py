from rest_framework import routers, serializers, viewsets, status, permissions, generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from .models import *
from io import StringIO
from .core.cryptkeeper import tools as cryptkeeper_tools
import json
from .core.crypto_price_finder import crypto_price_finder
from django.db.models import Sum
from datetime import datetime,timezone

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

### Spot Price ###
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

        success, price = crypto_price_finder.get_usd_price(
            target_time     = serializer.validated_data["datetime"],
            asset_symbol    = serializer.validated_data["asset_symbol"]
        )

        if not success:
            return Response("Request could not be completed.", status=400)
        
        return Response(price)

### Spot Price ###
class AssetInfoViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        asset_symbols = Transaction.objects.filter(user=request.user).values('asset_symbol').distinct()
        return Response(asset_symbols)

    #ex: http://localhost:8000/api/asset-info/btc/
    def retrieve(self, request, pk=None):
        asset_symbol = pk.upper()
        asset_transactions = Transaction.objects.filter(asset_symbol=asset_symbol, user=request.user) & (
            Transaction.objects.filter(transaction_type="Buy") |
            Transaction.objects.filter(transaction_type="Sell")
        )

        # Get spot price
        success, current_spot_price = crypto_price_finder.get_usd_price(
            asset_symbol    = asset_symbol
        )

        #Get totals
        total_asset_quantity        = float(asset_transactions.aggregate(Sum('asset_quantity'))["asset_quantity__sum"])
        total_active_invested       = float(asset_transactions.aggregate(Sum('usd_total_with_fees'))["usd_total_with_fees__sum"])

        # Calculate values based on spot price
        if success:
            current_asset_value             = float(total_asset_quantity or 0) * float(current_spot_price or 0)
            current_unrealized_profit_usd   = current_asset_value + float(total_active_invested or 0)
        else:
            current_asset_value = current_unrealized_profit_usd = 0

        result = {
            "asset_symbol"                          : asset_symbol,
            "total_asset_quantity"                  : total_asset_quantity,
            "total_active_invested"                 : total_active_invested,
            "current_spot_price"                    : current_spot_price,
            "current_asset_value"                   : current_asset_value,
            "current_unrealized_profit_usd"         : current_unrealized_profit_usd,
            "current_unrealized_profit_percentage"  : round(float(current_asset_value/abs(total_active_invested)), 2)
        }

        return Response(result)