# Generated by Django 4.2.3 on 2023-07-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_vendor_cac_file_remove_vendor_government_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='state',
            field=models.CharField(max_length=50),
        ),
    ]
