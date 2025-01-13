from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
import logging


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_key, item_data in bag.items():
        try:
            product_id, quality = item_key.split('_')
        except ValueError:
            raise ValueError(
                              f"Invalid bag key format: {item_key}. "
                              f"Expected 'product_id_quality'."
                            )

        product = get_object_or_404(Product, pk=product_id)

        quantity = item_data['quantity']
        price = Decimal(str(item_data['price']))

        total += quantity * price
        product_count += quantity
        bag_items.append({
            'item_id': item_key,
            'product': product,
            'quality': quality,
            'quantity': quantity,
            'price': price,
            'subtotal': quantity * price,
        })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
