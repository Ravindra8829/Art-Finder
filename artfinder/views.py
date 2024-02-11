from django.http import JsonResponse
from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.all()

    template_name = "home.html"
    context = {
        "products": products,
    }

    return render(request, template_name, context)


def update_cart(request):
    return JsonResponse("Item was added", safe=False)
