# Generated by Django 3.2.7 on 2021-10-08 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptkeeper', '0003_auto_20211008_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='usd_price_of_asset',
            field=models.DecimalField(decimal_places=2, max_digits=19),
        ),
    ]
