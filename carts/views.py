from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from category.models import Category
from .models import Cart, CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
  """
    Get the ID of the current session's cart.

    Args:
      request: The Django request object.

    Returns:
      str: The ID of the session's cart.
  """
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart


def add_cart(request, product_id):
  """
    Add a product to the cart.

    Args:
      request: The Django request object.
      product_id (int): The ID of the product to add.

    Returns:
      django.shortcuts.redirect: Redirect to the cart page.
  """
  # Get the product based on the ID
  product = Product.objects.get(id=product_id)
  product_variation = []
  
  if request.method == 'POST':
    for item in request.POST:
      key = item
      value = request.POST[key]
      try:
        # Check if the variation exists for the product
        variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
        # Add the variation to the product's variation list
        product_variation.append(variation)
      except:
        pass

  try:
    # Get the existing cart based on the session ID
    cart = Cart.objects.get(cart_id=_cart_id(request))
  except Cart.DoesNotExist:
    # Create a new cart if it doesn't exist
    cart = Cart.objects.create(cart_id = _cart_id(request))

  cart.save()

  # Check if the product with the same variations already exists in the cart
  cart_items = CartItem.objects.filter(product=product, cart=cart)
  added = False

  for cart_item in cart_items:
    existing_variations = cart_item.variations.all()
    if set(existing_variations) == set(product_variation):
      # Increase the quantity of the item in the cart
      cart_item.quantity += 1
      cart_item.save()
      added = True
      break

  if not added:
    # Create a new cart item with quantity 1
    cart_item = CartItem.objects.create(
      product=product,
      quantity=1,
      cart=cart,
    )
    if len(product_variation) > 0:
      # Add the selected variations to the cart item
      cart_item.variations.clear()
      cart_item.variations.add(*product_variation)
    cart_item.save()

  return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
  """
    Remove a product from the cart or decrease its quantity.

    Args:
      request: The Django request object.
      product_id (int): The ID of the product to remove from the cart.
      cart_item_id (int): The ID of the cart item to remove or decrease.

    Returns:
      django.shortcuts.redirect: Redirect to the cart page.
  """
  # Get the cart based on the session ID
  cart = Cart.objects.get(cart_id=_cart_id(request))
  # Get the product based on the ID
  product = get_object_or_404(Product, id=product_id)
  try:
    # Get the cart item corresponding to the product and cart item ID
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1:
      # Decrease the quantity of the cart item
      cart_item.quantity -= 1
      cart_item.save()
    else:
      # Completely remove the cart item
      cart_item.delete()
  except:
    pass
  return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
  """
    Completely remove a product from the cart.

    Args:
      request: The Django request object.
      product_id (int): The ID of the product to remove from the cart.
      cart_item_id (int): The ID of the cart item to remove.

    Returns:
      django.shortcuts.redirect: Redirect to the cart page.
  """
  # Get the cart based on the session ID
  cart = Cart.objects.get(cart_id=_cart_id(request))
  # Get the product based on the ID
  product = get_object_or_404(Product, id=product_id)
  # Get the cart item corresponding to the product and cart item ID
  cart_item = CartItem.objects.get(product=product, cart=cart.id, id=cart_item_id)
  # Completely remove the cart item
  cart_item.delete()
  return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
  """
    Display the shopping cart.

    Args:
      request: The Django request object.
      total (float): The total of the cart (default: 0).
      quantity (int): The total quantity of products in the cart (default: 0).
      cart_items (QuerySet): The cart items (default: None).

    Returns:
      django.shortcuts.render: Render the cart page.
  """
  tax = 0
  grand_total = 0
  try:
    # Get the cart based on the session ID
    cart = Cart.objects.get(cart_id=_cart_id(request))
    # Get all active cart items
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
      # Calculate the total by multiplying the product price by its quantity in the cart
      total += (cart_item.product.price * cart_item.quantity)
      # Calculate the total quantity of products in the cart
      quantity += cart_item.quantity
    # Calculate the tax by applying a fixed percentage (20%) on the total
    tax = (20 * total)/100
  except ObjectDoesNotExist:
    pass

  context = {
    'total': total,
    'quantity': quantity,
    'cart_items': cart_items,
    'tax': tax,
  }
  return render(request, 'store/cart.html', context)
