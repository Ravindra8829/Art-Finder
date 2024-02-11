# Generated by Django 4.0.3 on 2022-10-01 13:23

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='format: required, max-50', max_length=50, unique=True, verbose_name='category name')),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscore, or hyphens', unique=True, verbose_name='category safe URL')),
                ('description', models.TextField(blank=True, help_text='format: not required, max-1000', max_length=1000, verbose_name='category description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='format: required, max-255', max_length=255, verbose_name='name')),
                ('slug', models.SlugField(help_text='format: required, letters, numbers, underscores or hyphens', max_length=255, verbose_name='product safe URL')),
                ('description', models.TextField(help_text='format: required', verbose_name='product description')),
                ('price', models.DecimalField(decimal_places=2, error_messages={'name': {'max_length': 'the price must be between 0 and 99999.99.'}}, help_text='format: maximum price 99999.99', max_digits=7, verbose_name='price')),
                ('image', models.ImageField(help_text='Upload a product image', upload_to='images/', verbose_name='image')),
                ('thumbnail', models.ImageField(upload_to='thumbnails/', verbose_name='thumbnail')),
                ('alt_text', models.CharField(blank=True, help_text='Please add alternative text', max_length=255, null=True, verbose_name='Alternative text')),
                ('is_available', models.BooleanField(default=True, help_text='format: true=product available', verbose_name='product availability')),
                ('units', models.IntegerField(default=0, help_text='format: required, default-0', verbose_name='units')),
                ('units_sold', models.IntegerField(default=0, help_text='format: required, default-0', verbose_name='units sold to date')),
                ('trailer', models.FileField(blank=True, null=True, upload_to='trailers', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])])),
                ('created', models.DateTimeField(auto_now_add=True, help_text='format: Y-m-d H:M:S', verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, help_text='format: Y-m-d H:M:S', verbose_name='date product last updated')),
                ('category', models.ForeignKey(help_text='format: required', on_delete=django.db.models.deletion.PROTECT, related_name='products', to='products.category', verbose_name='category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=500)),
                ('rating', models.FloatField()),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent_data', models.CharField(blank=True, max_length=255, null=True)),
                ('thumbsup', models.IntegerField(default='0')),
                ('thumbsdown', models.IntegerField(default='0')),
                ('is_visible', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product')),
                ('thumbs', models.ManyToManyField(blank=True, default=None, related_name='thumbs', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='ReviewVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField(default=True)),
                ('review', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reviewid', to='products.review')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
