from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .forms import ProductForm
from .models import Product, Category, DeviceType  


def all_products(request):
    """ A view to show all products, including sorting and filtering """

    products = Product.objects.all()
    query = None
    category_filter = None
    device_type_filter = None
    sort = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            if sortkey == 'name_asc':
                sortkey = 'name'
            elif sortkey == 'name_desc':
                sortkey = '-name'
            elif sortkey == 'price_asc':
                sortkey = 'price'
            elif sortkey == 'price_desc':
                sortkey = '-price'
            elif sortkey == 'rating_asc':
                sortkey = 'rating'
            elif sortkey == 'rating_desc':
                sortkey = '-rating'

            sort = request.GET['sort']
            products = products.order_by(sortkey)


        if 'category' in request.GET:
            category_filter = request.GET['category']
            products = products.filter(category__name=category_filter)

        if 'device_type' in request.GET:
            device_type_filter = request.GET['device_type']
            products = products.filter(device_type__name=device_type_filter)

    categories = Category.objects.all()

    context = {
        'products': products,
        'search_term': query,
        'categories': categories,
        'current_sorting': sort,
        'category_filter': category_filter,
        'device_type_filter': device_type_filter,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)