from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
  """
    Custom AccountAdmin class that extends UserAdmin.

    This class customizes the Django UserAdmin interface for the Account model. It defines the fields to be displayed 
    in the list view, the fields to be linked to the object edit form, the read-only fields, and the ordering of the 
    objects in the list view. It also sets 'filter_horizontal', 'list_filter', and 'fieldsets' to empty, which can 
    be customized as needed.

    Attributes:
      list_display (tuple): Fields to be displayed in the list view.
      list_display_links (tuple): Fields to be linked to the object edit form.
      readonly_fields (tuple): Fields that will be read-only in the admin interface.
      ordering (tuple): Ordering of the objects in the list view.
      filter_horizontal (tuple): Fields to use for horizontal filters. Empty by default.
      list_filter (tuple): Fields to use for list filters. Empty by default.
      fieldsets (tuple): Configuration for fieldsets in the object edit form. Empty by default.
  """
  list_display       = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
  list_display_links = ('email', 'first_name', 'last_name')
  readonly_fields    = ('last_login', 'date_joined')
  ordering           = ('-date_joined',)

  filter_horizontal = ()
  list_filter       = ()
  fieldsets         = ()

# Register the Account model with the custom admin.
admin.site.register(Account, AccountAdmin)
