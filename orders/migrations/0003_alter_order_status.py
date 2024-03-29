# Generated by Django 4.0.3 on 2022-12-14 18:08

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderitem_vendor_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=django_fsm.FSMField(choices=[('created', 'Open'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('returned', 'Deferred')], default='created', max_length=50, protected=True),
        ),
    ]
