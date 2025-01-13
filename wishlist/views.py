from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):
    """
    Add a product to the user's wishlist
    """
    product = get_object_or_404(Product, pk=product_id)

    wishlist_exists = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).exists()

    if not wishlist_exists:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(
            request,
            f'{product.name} has been added to your wishlist!'
        )

    return redirect('product_detail', product_id=product.id)


@login_required
def wishlist_view(request):
    """
    View all products in the user's wishlist
    """
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(
        request,
        'wishlist/wishlist.html',
        {'wishlist_items': wishlist_items}
    )


@login_required
def remove_from_wishlist(request, item_id):
    """
    Remove a product from the user's wishlist
    """
    wishlist_item = get_object_or_404(Wishlist, pk=item_id, user=request.user)
    wishlist_item.delete()

    messages.success(
        request,
        'Product has been removed from your wishlist.'
    )

    return redirect('wishlist')
