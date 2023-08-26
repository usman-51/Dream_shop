from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
  """
    Context processor function to count the number of items in the cart.

    Args:
      request (HttpRequest): The request object used to generate this response.

    Returns:
      dict: A dictionary with a single key-value pair. The key 'cart_count' represents the total 
            quantity of items in the cart.

    Note:
      If the request path contains 'admin', an empty dictionary is returned.
      This is to prevent the cart count from appearing in the admin interface.
      If the Cart associated with the current session does not exist, 'cart_count' is set to 0.
  """
  cart_count = 0
  if 'admin' in request.path:
    return {}
  else:
    try:
      cart = Cart.objects.filter(cart_id=_cart_id(request))
      cart_items = CartItem.objects.all().filter(cart=cart[:1])
      for cart_item in cart_items:
        cart_count += cart_item.quantity
    except Cart.DoesNotExist:
      cart_count = 0
  return dict(cart_count=cart_count)
