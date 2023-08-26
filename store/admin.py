from django.contrib import admin
from .models import Product, Variation


class ProductAdmin(admin.ModelAdmin):
	"""
		Admin configuration for the Product model.
	
		Attributes:
			list_display (tuple): Fields to display in the admin list view.
			prepopulated_fields (dict): Fields to prepopulate based on other fields.
	"""
	list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
	prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
	"""
	    Admin configuration for the Variation model.
	
	    Attributes:
	      list_display (tuple): Fields to display in the admin list view.
	      list_editable (tuple): Fields that can be edited directly in the list view.
	      list_filter (tuple): Fields to use for filtering in the admin list view.
  	"""
	list_display = ('product', 'variation_category', 'variation_value', 'is_active')
	list_editable = ('is_active',)
	list_filter = ('product', 'variation_category', 'variation_value')

# Register the Product model with its corresponding admin configuration.
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
