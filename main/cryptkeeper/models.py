from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        BUY = 'Buy', _('Buy')
        SELL = 'Sell', _('Sell')
        INTEREST = 'Interest', _('Interest')

    transaction_type        = models.CharField(max_length=40,choices=TransactionType.choices)
    usd_transaction_fee     = models.DecimalField(max_digits=19, decimal_places=2, null=True)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_symbol            = models.CharField(max_length=50)
    usd_price               = models.DecimalField(max_digits=19, decimal_places=2)
    datetime                = models.DateTimeField()
    quantity                = models.DecimalField(max_digits=19, decimal_places=10)
    transaction_from        = models.CharField(max_length=50)
    transaction_to          = models.CharField(max_length=50)
    notes                   = models.CharField(max_length=200, null=True)
    import_hash             = models.CharField(max_length=100, null=True)

    readonly_fields = ["user"]

    def __str__(self):
        return f"{self.datetime} - {self.transaction_type} {self.quantity} {self.asset_symbol} for ${self.quantity * self.usd_price} at ${self.usd_price}/{self.asset_symbol}"