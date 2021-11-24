from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        BUY = 'Buy', _('Buy')
        SELL = 'Sell', _('Sell')
        INTEREST = 'Interest', _('Interest')
        SEND = 'Send', _('Send')
        AIRDROP = 'Airdrop', _('Airdrop')
        RECEIVE = 'Receive', _('Receive')

    user                    = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type        = models.CharField(max_length=40,choices=TransactionType.choices)
    usd_fee                 = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    asset_symbol            = models.CharField(max_length=50)
    spot_price              = models.DecimalField(max_digits=19, decimal_places=10)
    datetime                = models.DateTimeField()
    asset_quantity          = models.DecimalField(max_digits=19, decimal_places=10)
    transaction_from        = models.CharField(max_length=50)
    transaction_to          = models.CharField(max_length=50)
    notes                   = models.CharField(max_length=1000, null=True)
    import_hash             = models.CharField(max_length=100, null=True)
    #calculated fields
    usd_total_no_fees       = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    usd_total_with_fees     = models.DecimalField(max_digits=19, decimal_places=10, null=True)

    

    

    def save(self, *args, **kwargs):
        self.process_calculated_fields()
        super(Transaction, self).save(*args, **kwargs)

    def process_calculated_fields(self):
        #Examples:

        #Sell
        # quant: -5
        # cost $100
        # fee -$5
        # usd_total_no_fee == (quant * cost * -1) + fee == $495

        #Buy
        # quant: 5
        # cost $100
        # fee -$5
        # usd_total_no_fee == (quant * cost * -1) + fee == -$505

        #Send
        # quant: 5
        # cost $100
        # fee -$5
        # usd_total_no_fee == fee == -$5

        if (
            self.transaction_type == self.TransactionType.SEND or 
            self.transaction_type == self.TransactionType.INTEREST or 
            self.transaction_type == self.TransactionType.AIRDROP
        ):
            # Total is always zero + fees
            self.usd_total_no_fees = 0
            self.usd_total_no_fees = self.usd_total_with_fees
        else:
            self.usd_total_no_fees      = float(self.asset_quantity) * float(self.spot_price) * -1
            self.usd_total_with_fees    = self.usd_total_no_fees + float(self.usd_fee or 0)
        
    readonly_fields = ["user"]

    def __str__(self):
        return f"{self.datetime} - {self.transaction_type} {self.asset_quantity} {self.asset_symbol} for ${self.asset_quantity * self.spot_price} at ${self.spot_price}/{self.asset_symbol}"