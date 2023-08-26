from django.db import models
from django.urls import reverse

# Choices for the gender field.
GENDER_CHOICES = [
    ('H', 'Homme'),
    ('F', 'Femme'),
    ('O', 'Autre'),
]

# Choices for the product type field.
PRODUCT_TYPE_CHOICES = [
    ('Y', 'Accessoires Homme'),
    ('X', 'Accessoires Femme'),
    ('A', 'Vêtements Homme'),
    ('B', 'Vêtements Femme'),
    ('O', 'Autre'),
]


class Category(models.Model):
    """
		Represents a category of products.

		Attributes:
			category_name (CharField): The name of the category (max length: 50, unique).
			category_online (CharField): The online category name (max length: 50, default: empty string).
			slug (SlugField): The slug field for the category's URL (max length: 100, unique).
			description (TextField): The description of the category (max length: 255, blank).
			cat_image (ImageField): The image for the category (upload to: 'photos/categories', blank).
			gender (CharField): The gender for the category (max length: 1, choices: GENDER_CHOICES, default: empty string).
			product_type (CharField): The product type for the category (max length: 1, choices: PRODUCT_TYPE_CHOICES, default: empty string).
	"""
    category_name = models.CharField(max_length=50, unique=True)
    category_online = models.CharField(max_length=50, default="")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="")
    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPE_CHOICES, default="")

    class Meta:
        """
			verbose_name (str): The verbose name for the model.
      			verbose_name_plural (str): The verbose name in plural form for the model.
		"""
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        """
      			Returns the URL of the category.

		      	Returns:
				str: The URL of the category.
		"""
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        """
      			Returns a string representation of the category.

			Returns:
				str: The string representation of the category.
    		"""
        return self.category_name
