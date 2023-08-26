from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
  """
    Admin class for the Category model.

    Attributes:
      prepopulated_fields (dict): Specifies the fields that should be prepopulated based on other fields.
      list_display (tuple): Specifies the fields to be displayed in the list view of the admin site.
  """
  prepopulated_fields = {'slug': ('category_name',)}
  list_display = ('category_name', 'slug', 'gender', 'product_type')

# Register the Category model with the admin site using the CategoryAdmin class.
admin.site.register(Category, CategoryAdmin)
