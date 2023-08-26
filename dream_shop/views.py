from django.shortcuts import render
from store.models import Product
from category.models import Category


def home(request):
	"""
		Renders the home page with featured products and category links.

		Retrieves the best seller category and filters products that are available and belong to this category.
		Retrieves category links for women and men, as well as accessory categories for women and men.

		Returns:
			A rendered home page template with the featured products and category links.
	"""
	try:
		try:
			category = Category.objects.get(category_online="Best seller")
			products = Product.objects.filter(is_available=True, category=category)[:3]
		except Exception as e:
			print('----adfdf  dfkjahf alfa ',e )
			products = None
			pass
		women_links = Category.objects.filter(product_type='B')
		men_links = Category.objects.filter(product_type='A')

		women_acc = Category.objects.filter(product_type='X')
		men_acc = Category.objects.filter(product_type='Y')
	except Exception as e:
		print('-->>',e)
	context = {
			'products': products,
			'women_links': women_links,
			'women_acc': women_acc,
			'men_links': men_links,
			'men_acc': men_acc,
	}

	return render(request, 'home.html', context)
