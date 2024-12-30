from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm



def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key':'pk_test_51QWmVKK94uzNL5mlVxJ4TCPV8XP6MJcsGqUgxLrFS5akV4LYeYsJhvEt18MSO4knqa0Oh1eMciCgCG9vMmwK70oF00aEhOS5Ht',
        'client_secret':'test_client_secret',
    }

    return render(request, template, context)