from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from artfinder.utils import mk_paginator
from products.models import Product
from orders.models import Order

from .decorators import redirect_authenticated_user
from .models import User, Vendor
from .forms import (
    CustomerSignUpForm, VendorSignUpForm, UserForm,
    CustomerForm, VendorForm)


@redirect_authenticated_user
def vendor_signup(request):
    if request.method == "POST":
        form = VendorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Signup successful. Please wait for verification.")
            # Send welcome email to vendor
            return redirect("accounts:vendor")
        else:
            messages.warning(
                request, "An error occured. Please check below.")
    else:
        form = VendorSignUpForm()

    template_name = "vendor/signup.html"
    context = {
        "form": form,
        "user_type": "a vendor",
    }

    return render(request, template_name, context)


@redirect_authenticated_user
def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Your account was successfully created.")
            # Send welcome email to customer
            return redirect("home")
        else:
            messages.warning(
                request, "An error occured. Please check below.")
    else:
        form = CustomerSignUpForm()

    template_name = "registration/signup.html"
    context = {
        "form": form,
        "user_type": "a customer",
    }

    return render(request, template_name, context)


@login_required
def vendor_account(request):
    if request.user.is_customer:
        return redirect("accounts:customer")
    if request.method == 'POST':
        form = VendorForm(
            request.POST, request.FILES,
            instance=request.user.vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account was successully updated.')
            return redirect('accounts:vendor')
        else:
            messages.warning(
                request, 'There was an error while updating your account.')
    else:
        form = VendorForm(instance=request.user.vendor)

    template = 'vendor/account.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def customer_account(request):
    if request.user.is_vendor:
        return redirect("accounts:customer")
    if request.method == 'POST':
        user_form = UserForm(
            request.POST, instance=request.user)
        customer_form = CustomerForm(
            request.POST, request.FILES, instance=request.user.customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'Your account was successully updated.')
            return redirect('accounts:customer')
        else:
            messages.warning(
                request, 'There was an error while updating your account.')
    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=request.user.customer)

    template = 'customer/account.html'
    context = {
        'user_form': user_form,
        'customer_form': customer_form,
    }

    return render(request, template, context)


@login_required
def customer_orders(request):
    orders = Order.objects.filter(
        user=request.user)

    template = 'customer/orders.html'
    context = {
        'orders': orders,
        'orders_count': orders.count()

    }

    return render(request, template, context)


@login_required
def customer_addresses(request):

    template = 'customer/addresses.html'
    context = {
    }

    return render(request, template, context)


@login_required
def customer_wishlist(request):

    template = 'customer/wishlist.html'
    context = {
    }

    return render(request, template, context)


@login_required
def deactivate(request):
    user = request.user
    # disable the user's password
    user.set_unusable_password()
    # deactivate the user's account
    user.is_active = False
    user.save()
    logout(request)
    messages.success(
        request, "Your account has been successfully deactivated.")
    return redirect('home')


def vendor_profile(request, username):
    user = get_object_or_404(
        User, username=username)
    products = Product.objects.filter(
        vendor=user)
    product_count = products.count()
    products = mk_paginator(request, products, 4)

    template = 'vendor/profile.html'
    context = {
        'user': user,
        "products": products,
        "product_count": product_count,
    }

    return render(request, template, context)


def vendors(request):
    vendors = Vendor.objects.filter(is_verified=True)

    template = 'vendor/list.html'
    context = {
        "vendors": vendors,
    }

    return render(request, template, context)


@login_required
def vendor_products(request):
    products = Product.objects.filter(
        vendor=request.user)

    template = 'vendor/products.html'
    context = {
        "products": products,
    }

    return render(request, template, context)


@login_required
def vendor_orders(request):
    vendor = request.user.vendor
    orders = vendor.orders.all()
    # get only the items sold by a user in a particular order.

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True
        for item in order.items.all():
            if item.vendor_paid:
                order.vendor_paid_amount += item.get_cost()
            else:
                order.vendor_amount += item.get_cost()
                order.fully_paid = False

    template = 'vendor/orders.html'
    context = {
        'orders': orders,
        'vendor': vendor,
        'orders_count': orders.count()
    }

    return render(request, template, context)
