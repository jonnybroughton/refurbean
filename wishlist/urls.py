from django.urls import path
from bag.views import add_to_bag_from_wishlist
from . import views

urlpatterns = [
    path(
        '',
        views.wishlist_view,
        name='wishlist'
    ),
    path(
        'add-to-wishlist/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),
    path(
        'remove-from-wishlist/<int:item_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),
    path(
        'add-to-bag-from-wishlist/<int:product_id>/',
        add_to_bag_from_wishlist,
        name='add_to_bag_from_wishlist'
    ),
]
