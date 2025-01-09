from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from wishlist.models import Wishlist  # This imports Wishlist for accessing wishlist items

def view_bag(request):
    """ A view that renders the bag contents page """
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the specified amount """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id, None)
        messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect('view_bag')

def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """
    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id, None)
        messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.success(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

@login_required
def add_to_bag_from_wishlist(request, product_id):
    """ Add a product from the wishlist to the shopping bag """
    product = get_object_or_404(Product, pk=product_id)
    bag = request.session.get('bag', {})

    # Add the product to the shopping bag (default quantity = 1)
    quantity = 1

    if product_id in bag:
        bag[product_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[product_id]} in your bag.')
    else:
        bag[product_id] = quantity
        messages.success(request, f'Added {product.name} to your bag.')

    request.session['bag'] = bag
    return redirect('view_bag')  # Redirect to the bag page after adding
