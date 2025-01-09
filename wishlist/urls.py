from django.urls import path
from . import views

urlpatterns = [
    # URL to view the wishlist
    path('', views.wishlist_view, name='wishlist'),
    
    # URL to add a product to the wishlist
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    
    # URL to remove a product from the wishlist
    path('remove-from-wishlist/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist')


]
