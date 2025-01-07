from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ReviewForm
from .models import Product, Category, DeviceType, Review


def all_products(request):
    """ A view to show all products, including sorting and filtering """

    products = Product.objects.all()
    query = request.GET.get('q', None)
    category_filter = None
    device_type_filter = None
    sort = None

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

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


@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the product instance but don't commit it yet (to avoid FK errors)
            product = form.save(commit=False)

            # Save the product to generate the primary key (id)
            product.save()

            # Now that the product is saved, assign foreign key fields (category, device_type)
            if 'category' in form.cleaned_data:
                product.category = form.cleaned_data['category']
            if 'device_type' in form.cleaned_data:
                product.device_type = form.cleaned_data['device_type']

            # Save again to commit foreign key relationships
            product.save()

            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)





@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

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


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_review(request, product_id):
    """Add a review for a product"""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        rating = int(request.POST.get('rating'))
        
        if not 1 <= rating <= 5:
            messages.error(request, "Rating must be between 1 and 5.")
            return redirect(reverse('product_detail', args=[product_id]))

        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'title': title, 'content': content, 'rating': rating}
        )

        product.save()  # Recalculate the product's rating
        messages.success(request, "Your review has been saved.")
        return redirect(reverse('product_detail', args=[product_id]))


@login_required
def delete_review(request, review_id):
    """Delete a user's review"""
    review = get_object_or_404(Review, pk=review_id)

    if request.user == review.user or request.user.is_superuser:
        review.delete()
        review.product.save()  # Recalculate the product's rating
        messages.success(request, "Review deleted.")
    else:
        messages.error(request, "You cannot delete this review.")
    
    return redirect(reverse('product_detail', args=[review.product.id]))


@login_required
def edit_review(request, review_id):
    """ Edit a review for a product """
    review = get_object_or_404(Review, pk=review_id)

    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'products/edit_review.html', {
        'form': form,
        'review': review
    })
