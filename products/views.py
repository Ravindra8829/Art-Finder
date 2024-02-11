import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from carts.forms import CartAddProductForm
from artfinder.utils import mk_paginator

from .forms import ProductForm, ReviewForm
from .models import Category, Product, Review, ReviewVote


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    category = None
    products = Product.objects.filter(is_available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = category.products.filter(is_available=True)
    product_count = products.count()
    products = mk_paginator(request, products, 3)

    template_name = "products/list.html"
    context = {
        "products": products,
        "categories": categories,
        "category": category,
        "product_count": product_count,
    }

    return render(request, template_name, context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()
    reviews = product.reviews.filter(is_visible=True)

    # Check if the user has ordered for this item before
    # so that only users who have ordered item can post review
    # if request.user.is_authenticated:
    #     try:
    #         user_ordered_item = OrderItem.objects.filter(
    #             user=request.user, product_id=product.id).exists()
    #     except OrderItem.DoesNotExist:
    #         user_ordered_item = None
    # else:
    #     user_ordered_item = None

    # Get the review of the currently logged in user
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(
                user__id=request.user.id, product__slug=product.slug)
        except Review.DoesNotExist:
            user_review = None
    else:
        user_review = None

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.product = product
            review.ip = request.META.get('REMOTE_ADDR')
            review.user_agent_data = request.META.get('HTTP_USER_AGENT')
            review.save()
            messages.success(
                request, "Thanks! Your review was submitted successfully.")
            return redirect('products:detail', product.slug)
        else:
            messages.warning(
                request, "An error occured while submitting your form, check below")
    else:
        review_form = ReviewForm()

    similar_products = list(product.category.products.exclude(
        id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)

    template_name = "products/detail.html"
    context = {
        "product": product,
        "cart_product_form": cart_product_form,
        "reviews": reviews,
        "user_review": user_review,
        "review_form": review_form,
        "similar_products": similar_products,
    }

    return render(request, template_name, context)


def categories(request):
    categories = Category.objects.all()

    template_name = "products/categories.html"
    context = {
        "categories": categories,
    }

    return render(request, template_name, context)


def product_search(request):
    products = {}
    product_count = 0
    keyword = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(name__icontains=keyword)
            product_count = products.count()
            products = mk_paginator(request, products, 1)

    template_name = "products/search.html"
    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }

    return render(request, template_name, context)


# @vendor_required
def product_create(request):
    """ View to enable a Vendor upload a product. """
    if not request.user.vendor.is_verified:
        messages.success(
            request, 'Your account is yet to be verified, hence you can not upload a product.')
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user
            product.save()
            messages.success(
                request, "Your product has been successfully created.")
            return redirect(product)
    else:
        form = ProductForm()

    template_name = "products/form.html"
    context = {
        'form': form,
        'create': True,
    }

    return render(request, template_name, context)


def product_update(request, id):
    """ View to enable a Vendor update a product. """
    product = get_object_or_404(Product, id=id, vendor=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your product has been successfully updated.")
            return redirect(product)
    else:
        form = ProductForm(instance=product)

    template_name = "products/form.html"
    context = {
        'form': form,
    }

    return render(request, template_name, context)


def product_delete(request, id):
    # Use a Modal instead?
    product = get_object_or_404(Product, id=id, vendor=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(
            request, "Your product has been deleted.")
        return redirect(product)

    template_name = "products/delete.html"
    context = {
        'product': product,
    }

    return render(request, template_name, context)


@login_required
def vote_review(request):
    if request.POST.get("action") == "thumbs":
        id = int(request.POST.get("reviewid"))
        button = request.POST.get("button")
        update = Review.objects.get(id=id)

        # Check if user has made vote
        if update.thumbs.filter(id=request.user.id).exists():

            # Get the users current vote (T/F)
            q = ReviewVote.objects.get(Q(
                review_id=id) & Q(user_id=request.user.id))
            user_vote = q.vote

            if user_vote is True:
                # If user presses thumbs up again
                if button == "thumbsup":
                    update.thumbsup = F("thumbsup") - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    # delete the previous thumb action
                    q.delete()

                    return JsonResponse(
                        {"up": up, "down": down, "remove": "none"})

                if button == "thumbsdown":
                    # Change vote
                    update.thumbsup = F("thumbsup") - 1
                    update.thumbsdown = F("thumbsdown") + 1
                    update.save()

                    # Update vote
                    q.vote = False
                    q.save(update_fields=["vote"])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({"up": up, "down": down})

            pass

            if user_vote is False:
                if button == "thumbsup":
                    # Change vote in review
                    update.thumbsup = F("thumbsup") + 1
                    update.thumbsdown = F("thumbsdown") - 1
                    update.save()

                    # Update vote
                    q.vote = True
                    q.save(update_fields=["vote"])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({"up": up, "down": down})

                # If user presses thumbs down again
                if button == "thumbsdown":
                    update.thumbsdown = F("thumbsdown") - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse(
                        {"up": up, "down": down, "remove": "none"})

        else:
            # New selection
            if button == "thumbsup":
                update.thumbsup = F("thumbsup") + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = ReviewVote(
                    review_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                # Thumbsdown
                update.thumbsdown = F("thumbsdown") + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = ReviewVote(
                    review_id=id, user_id=request.user.id, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({"up": up, "down": down})
    pass
