from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
import datetime
from carts.cart import Cart

from .models import OrderItem, Order
from .forms import OrderCreateForm


def notify_customer(order):
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for your order.'
    html_content = render_to_string('orders/email_notify_customer.html', {'order': order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def notify_vendor(order):
    from_email = settings.DEFAULT_FROM_EMAIL
    for vendor in order.vendors.all():
        to_email = vendor.user.email
        subject = 'New Order'
        text_content = 'You have a new order.'
        html_content = render_to_string('orders/email_notify_vendor.html', {'order': order, 'vendor': vendor})
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            for item in cart:
                if request.user.is_authenticated:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        user=request.user,
                        # vendor=item['product'].vendor,
                        vendor=item['product'].vendor.vendor,
                        vendor_paid=True,
                        quantity=item['quantity'])
                    # order.vendors.add(item['product'].vendor)
                    order.vendors.add(item['product'].vendor.vendor)
                else:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        vendor_paid=True,
                        vendor=item['product'].vendor.vendor,
                        quantity=item['quantity'])
                    order.vendors.add(item['product'].vendor.vendor)

            # clear the cart
            cart.clear()

            # Send email
            notify_customer(order)
            notify_vendor(order)

            # return a redirect instead; get the order id from user session
            return render(request,
                          'orders/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm()
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': request.user.customer.address,
                'phone_number': request.user.customer.phone_number,
                'postal_code': request.user.customer.postal_code,
                'city': request.user.customer.city,
            }
            form = OrderCreateForm(initial=initial_data)
    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


@login_required
def track_order(request, id):
    order = get_object_or_404(Order, id=id)

    return render(
        request, 'orders/track_order.html', {'order': order})


@login_required
def order_status_shipped(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.SHIPPED
    order.save()
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = order.email
    send_mail(
        'Order Status Information',
        'Hi there, your order status has been changed to: SHIPPED',
        from_email,
        [to_email],
        fail_silently=False,
    )
    messages.success(
        request, "Order status changed to: Shipped")
    return redirect(current_url)


@login_required
def order_status_processing(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.PROCESSING
    order.save()
    messages.success(
        request, "Order status changed to: Processing")
    return redirect(current_url)


@login_required
def order_status_completed(request, id):
    order = get_object_or_404(Order, id=id)
    current_url = request.META['HTTP_REFERER']
    order.status = order.COMPLETED
    order.save()
    messages.success(
        request, "Order status changed to: Completed")
    return redirect(current_url)
