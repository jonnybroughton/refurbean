from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, DeviceType  # Import the DeviceType model

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    category_filter = None  # To store the selected category
    device_type_filter = None  # To store the selected device type

    # Search functionality
    if request.GET.get('q'):
        query = request.GET['q']
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        else:
            messages.error(request, "You didn't enter any search criteria!")

    # Category filtering
    if request.GET.get('category'):
        category_filter = request.GET['category']
        products = products.filter(category__name=category_filter)

    # Device Type filtering
    if request.GET.get('device_type'):
        device_type_filter = request.GET['device_type']
        products = products.filter(device_type__name=device_type_filter)

    context = {
        'products': products,
        'search_term': query,
        'category_filter': category_filter,
        'device_type_filter': device_type_filter,  # To show which device type is selected
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
