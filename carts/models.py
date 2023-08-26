from django.db import models
from store.models import Product, Variation


class Cart(models.Model):
  """
    Represents a shopping cart.

    Attributes:
      cart_id (CharField): A unique identifier for the cart. Can be blank.
      date_added (DateField): The date the cart was created. Automatically set to the current date.
  """
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)


  def __str__(self):
    """
      Returns a string representation of the cart.

      Returns:
        str: The unique identifier of the cart.
    """
    return self.cart_id



class CartItem(models.Model):
  """
    Represents an item in a shopping cart.

    Attributes:
      product (ForeignKey): The product in the cart. On product deletion, the cart item is also deleted.
      variations (ManyToManyField): Any variations of the product. Can be blank.
      cart (ForeignKey): The cart the item belongs to. On cart deletion, the cart item is also deleted.
      quantity (IntegerField): The quantity of the product in the cart.
      is_active (BooleanField): Whether the cart item is active. Default is True.
  """
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  variations = models.ManyToManyField(Variation, blank=True)
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  is_active = models.BooleanField(default=True)


  def sub_total(self):
    """
      Calculates the total price for this item (product price * quantity).

      Returns:
        float: The total price for this item.
    """
    return self.product.price * self.quantity


  def __str__(self):
    """
      Returns a string representation of the cart item.

      Returns:
        str: The string representation of the product.
    """
    return str(self.product)
