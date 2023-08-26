from django.test import TestCase
from store.models import Product, Variation
from category.models import Category
from django.conf import settings
from django.core.exceptions import ValidationError


class ProductModelTest(TestCase):
  """
    Test class for the Product model.

    Methods:
      setUp: Set up environment for each test.
      test_product_creation: Test if a product is created successfully.
      test_product_url: Test if the get_url method returns the expected URL for the product.
      test_product_has_name: Test if the product has a correctly defined name.
      test_product_has_title_online: Test if the product has a correctly defined online title.
      test_product_has_slug: Test if the product has a correctly defined slug.
      test_product_has_description: Test if the product has a correctly defined description.
      test_product_has_price: Test if the product has a correctly defined price.
      test_product_has_positive_price: Test if the product price is positive.
      test_product_has_valid_stock: Test if the product stock is a positive number.
      test_product_has_stock: Test if the product has a correctly defined stock.
      test_product_is_available: Test if the product is available (default: True).
      test_product_has_category: Test if the product has a correctly defined associated category.
      test_product_has_created_date: Test if the product has a defined creation date.
      test_product_has_modified_date: Test if the product has a defined modification date.
      test_product_variation_count: Test the number of variations associated with the product (in this example, one variation).
      test_product_str: Test if the __str__ method of the Product model returns the product name.
      test_product_has_images: Test if the product has correctly configured images.
      test_product_has_no_second_image: Test if the product does not have a second image.
      test_product_get_url: Test if the get_url method returns the correct URL for the product.
      test_product_variation_category_choices: Test if the variation_category only accepts valid choices.
  """
  def setUp(self):
    """
      Set up environment for each test.

      Creates a test category and a test product with an associated variation.
    """
    category = Category.objects.create(category_name='Test category', slug='test-category')

    self.product = Product.objects.create(
      product_name='Test product',
      title_online='Test title',
      slug='test-product',
      description='Test description',
      price=10.0,
      stock=5,
      category=category
    )
    Variation.objects.create(
      product=self.product,
      variation_category='color',
      variation_value='Red',
      is_active=True
    )
  

  def test_product_creation(self):
    """
      Test if a product is created successfully.

      Asserts that the product is an instance of the Product model.
    """
    self.assertTrue(isinstance(self.product, Product))
    self.assertEqual(str(self.product), 'Test product')


  def test_product_url(self):
    """
      Test if the product URL is generated correctly.

      This method asserts that the generated URL for the product matches the expected URL.
    """
    expected_url = '/store/category/test-category/test-product/'
    self.assertEqual(self.product.get_url(), expected_url)


  def test_product_has_name(self):
    """
      Test if the product has the correct name.

      This method asserts that the product's name matches the expected name.
    """
    self.assertEqual(self.product.product_name, 'Test product')


  def test_product_has_title_online(self):
    """
      Test if the product has the correct online title.

      This method asserts that the product's online title matches the expected title.
    """
    self.assertEqual(self.product.title_online, 'Test title')


  def test_product_has_slug(self):
    """
      Test if the product has the correct slug.

      This method asserts that the product's slug matches the expected slug.
    """
    self.assertEqual(self.product.slug, 'test-product')


  def test_product_has_description(self):
    """
      Test if the product has the correct description.

      This method asserts that the product's description matches the expected description.
    """
    self.assertEqual(self.product.description, 'Test description')


  def test_product_has_price(self):
    """
      Test if the product has the correct price.

      This method asserts that the product's price matches the expected price.
    """
    self.assertEqual(self.product.price, 10.0)


  def test_product_has_positive_price(self):
    """
      Test if the product has a positive price.

      This method asserts that the product's price is greater than zero.
    """
    self.assertGreater(self.product.price, 0)


  def test_product_has_valid_stock(self):
    """
      Test if the product has a valid stock.

      This method asserts that the product's stock is greater than zero.
    """
    self.assertGreater(self.product.stock, 0)


  def test_product_has_stock(self):
    """
      Test if the product has the correct stock.

      This method asserts that the product's stock matches the expected stock.
    """
    self.assertEqual(self.product.stock, 5)


  def test_product_is_available(self):
    """
      Test if the product is available.

      This method asserts that the product is marked as available (True).
    """
    self.assertTrue(self.product.is_available)


  def test_product_has_category(self):
    """
      Test if the product has the correct category.

      This method asserts that the product's category matches the expected category.
    """
    category = Category.objects.get(category_name='Test category')
    self.assertEqual(self.product.category, category)


  def test_product_has_created_date(self):
    """
      Test if the product has a created date.

      This method asserts that the product's created date is not None.
    """
    self.assertIsNotNone(self.product.created_date)


  def test_product_has_modified_date(self):
    """
      Test if the product has a modified date.

      This method asserts that the product's modified date is not None.
    """
    self.assertIsNotNone(self.product.modified_date)


  def test_product_variation_count(self):
    """
      Test the count of variations associated with the product.

      This method asserts the count of variations associated with the product.
      In this example, there should be one variation.
    """
    self.assertEqual(self.product.variation_set.count(), 1)


  def test_product_str(self):
    """
      Test the string representation of the product.

      This method asserts that the string representation of the product matches the expected value.
    """
    self.assertEqual(str(self.product), 'Test product')


  def test_product_has_images(self):
    """
      Test if the product has correctly configured images.

      This method asserts that the product's images have the correct file path and URL.
    """
    image_path = 'photos/products/test-product.jpg'
    self.product.images.name = image_path
    self.product.save()
    self.assertEqual(self.product.images.path, f'{settings.MEDIA_ROOT}/{image_path}')
    self.assertEqual(self.product.images.url, f'{settings.MEDIA_URL}{image_path}')


  def test_product_has_no_second_image(self):
    """
      Test if the product has no second image.

      This method asserts that the product's second image field is False (empty).
    """
    self.assertFalse(self.product.second_image)


  def test_product_get_url(self):
    """
      Test if the product's get_url method returns the correct URL.

      This method asserts that the get_url method of the product returns the expected URL.
    """
    expected_url = '/store/category/test-category/test-product/'
    self.assertEqual(self.product.get_url(), expected_url)


  def test_product_variation_category_choices(self):
    """
      Test if the product variation category only accepts valid choices.

      This method creates an invalid variation with an invalid category and asserts that a ValidationError is raised.
    """
    invalid_variation = Variation.objects.create(
        product=self.product,
        variation_category='invalid_category',
        variation_value='Value',
        is_active=True
    )
    with self.assertRaises(ValidationError) as context:
        invalid_variation.clean_fields()
    exception_message = str(context.exception)
    self.assertIn("invalid_category", exception_message)
