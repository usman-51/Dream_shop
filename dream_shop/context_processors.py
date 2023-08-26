from category.models import Category


def category_links(request):
	"""
    Retrieve category links for display on a page.

    Returns:
      A dictionary containing the following category links:
      - women_links: Women's links (product_type='B')
      - women_acc: Women's accessories (product_type='X')
      - men_links: Men's links (product_type='A')
      - men_acc: Men's accessories (product_type='Y')
      - men_links_all: All men's links (gender='H')
      - women_links_all: All women's links (gender='F')
  """
	women_links = Category.objects.filter(product_type='B')
	men_links = Category.objects.filter(product_type='A')
	women_acc = Category.objects.filter(product_type='X')
	men_acc = Category.objects.filter(product_type='Y')
	men_links_all = Category.objects.filter(gender='H')
	women_links_all = Category.objects.filter(gender='F')

	return {
			'women_links': women_links,
			'women_acc': women_acc,
			'men_links': men_links,
			'men_acc': men_acc,
			'men_links_all': men_links_all,
			'women_links_all': women_links_all,
	}
