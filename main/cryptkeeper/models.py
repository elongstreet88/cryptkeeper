from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        FRESHMAN = 'Buy', _('Buy')
        SOPHOMORE = 'Sell', _('Sell')

    transaction_type        = models.CharField(max_length=4,choices=TransactionType.choices)
    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    asset_symbol            = models.CharField(max_length=50)
    usd_price               = models.DecimalField(max_digits=19, decimal_places=2)
    datetime                = models.DateTimeField()
    quantity                = models.DecimalField(max_digits=19, decimal_places=8)

    def __str__(self):
        return f"{self.datetime} - {self.transaction_type} {self.quantity} {self.asset_symbol} for ${self.quantity * self.usd_price} at ${self.usd_price}/{self.asset_symbol}"