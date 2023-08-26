from django.apps import AppConfig


class StoreConfig(AppConfig):
	"""
	Configuration class for the 'store' application.

	Attributes:
		Default_auto_field (str): The default automatic field type for model primary keys.
		Name (str): The name of the 'store' application.
	"""
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'store'
