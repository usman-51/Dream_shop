from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
	Configuration class for the 'accounts' Django application.

	Attributes:
		default_auto_field (str): Specifies the type of auto-created primary key field 
			for models in the 'accounts' application. Set to 'django.db.models.BigAutoField'.
	name (str): The name of the application, 'accounts'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
