from django.apps import AppConfig


class CategoryConfig(AppConfig):
	"""
		Configuration class for the Category app.

		Attributes:
			default_auto_field (str): Specifies the default auto-generated field type for models.
			name (str): Specifies the name of the app.
	"""
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'category'
