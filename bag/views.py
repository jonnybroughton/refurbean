from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from wishlist.models import Wishlist


def view_bag(request):
    """ Render the shopping bag page """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    quality = request.POST.get('quality')
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    price = None

    if quality == 'fair':
        price = product.price
    elif quality == 'good':
        price = product.price_good
    elif quality == 'amazing':
        price = product.price_amazing

    if price is None:
        messages.error(
            request,
            f"Price for quality '{quality}' "
            f"is not available for this product."
        )
        return redirect(redirect_url)

    item_key = f"{item_id}_{quality}"
    if item_key in bag:
        bag[item_key]['quantity'] += quantity
    else:
        bag[item_key] = {
            'quantity': quantity,
            'quality': quality,
            'price': str(price),
        }

    request.session['bag'] = bag
    messages.success(
        request,
        f'Added {product.name} ({quality.capitalize()}) '
        f'to your bag'
    )
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of a product in the shopping bag """
    try:
        product_id, quality = item_id.split('_')
    except ValueError:
        messages.error(request, "Invalid item key format.")
        return redirect('view_bag')

    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})
    item_key = f"{product_id}_{quality}"

    if item_key in bag:
        if quantity > 0:
            bag[item_key]['quantity'] = quantity
            messages.success(
                request,
                f'Updated {product.name} ({quality}) quantity to {quantity}'
            )
        else:
            del bag[item_key]
            messages.success(
                request,
                f'Removed {product.name} ({quality}) from your bag'
            )
    else:
        messages.error(
            request,
            f"Could not find {product.name} ({quality}) in your bag."
        )

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, item_id):
    """ Remove a product from the shopping bag """
    try:
        product_id, quality = item_id.split('_')
        product = get_object_or_404(Product, pk=product_id)
        bag = request.session.get('bag', {})
        item_key = f"{product_id}_{quality}"

        if item_key in bag:
            del bag[item_key]
            messages.success(
                request,
                f'Removed {product.name} ({quality}) '
                f'from your bag'
            )
        else:
            messages.error(
                request,
                f"Item {product.name} ({quality})"
                f"not found in your bag"
            )

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


@login_required
def add_to_bag_from_wishlist(request, product_id):
    """ Add a product from the wishlist to the shopping bag """
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        bag = request.session.get('bag', {})
        quality = request.POST.get('quality')
        quantity = int(request.POST.get('quantity', 1))
        price = None

        if quality == 'fair':
            price = product.price
        elif quality == 'good' and hasattr(product, 'price_good'):
            price = product.price_good
        elif quality == 'amazing' and hasattr(product, 'price_amazing'):
            price = product.price_amazing

        if price is None:
            messages.error(
                request,
                f"Price for quality '{quality}' "
                f"is not available for this product."
            )
            return redirect('wishlist')

        item_key = f"{product_id}_{quality}"
        if item_key in bag:
            bag[item_key]['quantity'] += quantity
        else:
            bag[item_key] = {
                'quantity': quantity,
                'quality': quality,
                'price': str(price),
            }

        request.session['bag'] = bag
        messages.success(
            request,
            f'{product.name} ({quality.capitalize()}) '
            f'has been added to your bag!'
        )

    return redirect('wishlist')
