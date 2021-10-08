# Generated by Django 3.2.7 on 2021-10-08 02:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cryptkeeper', '0002_auto_20211008_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell')], max_length=4)),
                ('asset_symbol', models.CharField(max_length=50)),
                ('usd_price_of_asset', models.DecimalField(decimal_places=8, max_digits=19)),
                ('datetime_of_transaction', models.DateTimeField()),
                ('quantity_of_transaction', models.DecimalField(decimal_places=8, max_digits=19)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='selltransaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='BuyTransaction',
        ),
        migrations.DeleteModel(
            name='SellTransaction',
        ),
    ]
