# Generated by Django 4.0.3 on 2022-12-17 23:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
