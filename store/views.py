from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse


def store(request, category_slug=None):
    """
        View for displaying the main page of the store.

        Arguments:
        request -- HTTP request
        category_slug -- Category slug (default: None)
        
        Returns:
        HTTP response with the rendering of the store page
    """
    # Initializing the variables
    categories = None
    products = None
    page_title = "Collection Complète"

    # If a category slug is provided
    if category_slug is not None:
        # Retrieve the corresponding category or raise a 404 error if it doesn't exist
        categories = get_object_or_404(Category, slug=category_slug)
        
        # Filter the available products based on this category
        products = Product.objects.filter(category=categories, is_available=True)

        # Paginator for the store page with 9 items per page
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
        # Count the number of available products in this category
        product_count = products.count()
        page_title = categories.category_name
    else:
        # If no category slug is provided, retrieve all available products
        products = Product.objects.filter(is_available=True).order_by('id')

        # Filter the products by gender (male or female) and by product type
        gender = request.GET.get('gender')
        category = request.GET.get('category')
        if gender == 'men':
            products = products.filter(category__gender='H')
            page_title = "Collection Homme"
        elif gender == 'women':
            products = products.filter(category__gender='F')
            page_title = "Collection Femme"
        
        if category == 'clothingMen':
            products = products.filter(category__product_type='A')
            page_title = "Vêtements Homme"
        elif category == 'clothingWomen':
            products = products.filter(category__product_type='B')
            page_title = "Vêtements Femme"
        elif category == 'clothingAccessMen':
            products = products.filter(category__product_type='Y')
            page_title = "Accessoires Homme"
        elif category == 'clothingAccessWomen':
            products = products.filter(category__product_type='X')
            page_title = "Accessoires Femme"

        # Pagination of the store with 9 items per page
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        # Count the total number of available products
        product_count = products.count()

    # Create the context with the products, the number of products, and the page title
    context = {
        'products': paged_products,
        'product_count': product_count,
        'page_title': page_title,
    }

    # Render the store page with the created context
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    """
        View to display the details of a specific product.
    """
    try:
        # Retrieve the specific product or raise an exception if it does not exist.
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # Create the context with the product and category links.
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }

    # Render the product detail page with the created context.
    return render(request, 'store/product_detail.html', context)


def search(request):
    # Check if the keyword is present in the GET request.
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # Si le mot-clé n'est pas vide
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            # Count the total number of found products.
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
