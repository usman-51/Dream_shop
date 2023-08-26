from django.apps import AppConfig


class CartsConfig(AppConfig):
	"""
		Configuration class for the 'carts' Django application.

		Attributes:
			default_auto_field (str): Specifies the type of auto-created primary key field 
					for models in the 'carts' application. Set to 'django.db.models.BigAutoField'.
			name (str): The name of the application, 'carts'.
	"""
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'carts'
