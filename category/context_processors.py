from .models import Category


def menu_links(request):
	"""
		Retrieves the menu links for the navigation bar.

		Args:
			request (HttpRequest): The HTTP request object.

		Returns:
			dict: A dictionary containing the menu links.
	"""
	links = Category.objects.exclude(category_name="Best Seller")
	return dict(links=links)
