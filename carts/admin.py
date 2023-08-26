from django.contrib import admin
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
  """
    Configuration class for the Cart model in the Django admin interface.

    Attributes:
      list_display (tuple): Specifies the fields to be displayed as columns in the Cart model list.
  """
  list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
  """
    Configuration class for the CartItem model in the Django admin interface.

    Attributes:
      list_display (tuple): Specifies the fields to be displayed as columns in the CartItem model list.
  """
  list_display = ('product', 'cart', 'quantity', 'is_active')

# Register the Cart and CartItem models in the admin interface
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
