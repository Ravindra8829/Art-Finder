# from django.core.validators import MinLengthValidator, MaxLengthValidator
# from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_vendor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)


class Vendor(models.Model):
    """ Vendor model for storing vendor information. """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='vendor')
    company_name = models.CharField(max_length=50)
    address = models.CharField(max_length=600)
    about = models.TextField()
    state = models.CharField(max_length=50)
    image = models.ImageField(upload_to='vendor/images')
    phone_number = models.CharField(max_length=11)
    #     validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    # shop_logo = models.ImageField('logo', null=True, blank=True)
    # phone_regex = RegexValidator(
    #     regex=r'^\+?234?\d{10,11}$',
    #     message="Phone number must be entered in the format:
    #               '+2341234233566'. Up to 11 digits allowed.")
    # mobile_number = models.CharField(
    #     validators=[phone_regex], max_length=17, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='customer')
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    image = models.ImageField(
        upload_to='customer/images', blank=True, null=True)
    address = models.CharField(
        max_length=250, blank=True, null=True)
    postal_code = models.CharField(
        max_length=5, blank=True, null=True)
    city = models.CharField(
        max_length=20, blank=True, null=True)
    # country = models.CharField(max_length=100, blank=True)
    state = models.CharField(
        max_length=20, blank=True, null=True)

    @property
    def email(self):
        return f"{self.user.email}"

    def __str__(self):
        return f"{self.user.username} profile"
