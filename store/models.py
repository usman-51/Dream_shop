from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
	"""
	    Model representing a product in the system.
	
	    Attributes:
	      product_name (CharField): The name of the product (max_length: 200, unique).
	      title_online (CharField): The online title of the product (max_length: 200, default: '').
	      slug (SlugField): The slug for the product's friendly URL (max_length: 200, unique).
	      description (TextField): The description of the product (max_length: 500, blank).
	      price (FloatField): The price of the product (default: 0.0).
	      images (ImageField): The images of the product (upload_to: 'photos/products', blank, null).
	      second_image (ImageField): The second image for the reverse of full collection products (upload_to: 'photos/products', blank, null).
	      third_image (ImageField): The third image for the reverse of full collection products (upload_to: 'photos/products', blank, null).
	      fourth_image (ImageField): The fourth image for the reverse of full collection products (upload_to: 'photos/products', blank, null).
	      fifth_image (ImageField): The fifth image for the reverse of full collection products (upload_to: 'photos/products', blank, null).
	      stock (IntegerField): The available stock of the product (default: 0).
	      is_available (BooleanField): The availability indicator of the product (default: True).
	      category (ForeignKey): The category of the product (relation with Category model, on_delete: models.CASCADE).
	      created_date (DateTimeField): The creation date of the product (auto_now_add: True).
	      modified_date (DateTimeField): The modification date of the product (auto_now: True).
  	"""
	product_name = models.CharField(max_length=200, unique=True)
	title_online = models.CharField(max_length=200, default='')
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(max_length=500, blank=True)
	price = models.FloatField(default=0.0)
	images = models.ImageField(upload_to='photos/products', blank=True, null=True)
	second_image = models.ImageField(upload_to='photos/products', blank=True, null=True)
	third_image = models.ImageField(upload_to='photos/products', blank=True, null=True)
	fourth_image = models.ImageField(upload_to='photos/products', blank=True, null=True)
	fifth_image = models.ImageField(upload_to='photos/products', blank=True, null=True)
	stock = models.IntegerField(default=0)
	is_available = models.BooleanField(default=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)


	def get_url(self):
		"""
		      Returns the URL of the product.
		
		      Returns:
		        str: The URL of the product.
    		"""
		return reverse('product_detail', args=[self.category.slug, self.slug])


	def __str__(self):
		"""
      			Returns a string representation of the product.
    		"""
		return self.product_name



class VariationManager(models.Manager):
	"""
	    Manager class for handling variations.
	
	    Methods:
	      colors: Retrieve all active color variations.
	      sizes: Retrieve all active size variations.
    	"""
	def colors(self):
		"""
		      Retrieve all active color variations.
		
		      Returns:
		        QuerySet: All active color variations.
    		"""
		return super(VariationManager, self).filter(variation_category='color', is_active=True)


	def sizes(self):
		"""
		      Retrieve all active size variations.
		
		      Returns:
		        QuerySet: All active size variations.
    		"""
		return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
	"""
	    Model representing a variation of a product.
	
	    Attributes:
	      product (ForeignKey): The product to which the variation is associated (relation with Product model, on_delete: models.CASCADE).
	      variation_category (CharField): The category of the variation (max_length: 100, choices: variation_category_choice).
	      variation_value (CharField): The value of the variation (max_length: 100).
	      is_active (BooleanField): The activation indicator of the variation (default: True).
	      created_date (DateTimeField): The creation date of the variation (auto_now: True).
	
	    Managers:
	      objects (VariationManager): The manager for variations.
  	"""
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variation_category = models.CharField(max_length=100, choices=variation_category_choice)
	variation_value = models.CharField(max_length=100)
	is_active =  models.BooleanField(default=True)
	created_date = models.DateTimeField(auto_now=True)

	objects = VariationManager()

	def __str__(self):
		"""
      			Returns a string representation of the variation.
    		"""
		return self.variation_value
