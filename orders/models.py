from datetime import datetime, timedelta
from django.db import models
from django_fsm import FSMField, transition
from accounts.models import User, Vendor
from products.models import Product


# class STATUS(models.TextChoices):
#     CREATED = 'created', 'Open'
#     PROCESSING = 'processing', 'Processing'
#     SHIPPED = 'shipped', 'Shipped'
#     COMPLETED = 'completed', 'Completed'
#     CANCELLED = 'cancelled', 'Cancelled'
#     RETURNED = 'returned', 'Deferred'

class Order(models.Model):
    CREATED = 'Created'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    COMPLETED = 'Completed'
    # CANCELLED = 'Cancelled'
    # RETURNED = 'Returned'
    ORDER_STATUS = [
        (CREATED, 'Created'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
    ]
    #     (CANCELLED, 'Cancelled'),
    #     (RETURNED, 'Returned'),
    # ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders',
        blank=True, null=True) # models.SET_NULL
    # full_name?
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    # address1 / address2?
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(
        choices=ORDER_STATUS, max_length=10, default=CREATED)
    # status = FSMField(choices=STATUS.choices, default=STATUS.CREATED)
    note = models.TextField(blank=True)
    delivery_date = models.DateTimeField(default=datetime.now()+timedelta(days=4))
    # transaction_id = models.CharField(max_length=200, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, related_name='orders')

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    # @transition(field=status, source=STATUS.CREATED, target=STATUS.PROCESSING)
    # def created_to_processing(self):
    #     self.status = STATUS.PROCESSING

    # @transition(field=status, source=STATUS.PROCESSING, target=STATUS.SHIPPED)
    # def processing_to_shipped(self):
    #     self.status = STATUS.SHIPPED

    # @transition(field=status, source=STATUS.SHIPPED, target=STATUS.COMPLETED)
    # def shipped_to_completed(self):
    #     self.status = STATUS.COMPLETED

    @transition(field=status, source=CREATED, target=PROCESSING)
    def created_to_processing(self):
        self.status = self.PROCESSING

    @transition(field=status, source=PROCESSING, target=SHIPPED)
    def processing_to_shipped(self):
        self.status = self.SHIPPED

    @transition(field=status, source=SHIPPED, target=COMPLETED)
    def shipped_to_completed(self):
        self.status = self.COMPLETED


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='orderitems',
        blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, related_name='items',
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vendor_paid = models.BooleanField(default=False)
    # status?

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
