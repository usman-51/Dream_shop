from django.test import TestCase
from category.models import Category
from django.urls import reverse
import os


class CategoryModelTest(TestCase):
  """
    Test class for the Category model.

    Methods:
      setUp: Set up the environment for each test.
      test_category_creation: Test if a category is created successfully.
      test_category_url: Test the get_url method of the Category model.
      test_category_has_name: Test if the category has the correct name.
      test_category_has_slug: Test if the category has the correct slug.
      test_category_has_description: Test if the category has an empty description by default.
      test_category_has_image: Test if the category has an empty image by default.
      test_category_has_gender: Test if the category has an empty gender by default.
      test_category_has_product_type: Test if the category has an empty product type by default.
      test_category_str: Test the __str__ method of the Category model.
      test_category_get_url: Test the get_url method of the Category model.
      test_category_online_default_value: Test if the category has an empty category_online by default.
      test_category_description_blank: Test if a category's description can be blank.
      test_category_gender_choices: Test the gender choices for a category.
      test_category_product_type_choices: Test the product type choices for a category.
      test_category_description_max_length: Test the maximum length of a category's description.
      test_category_image_upload: Test uploading an image for a category.
    """
  def setUp(self):
    """
      Set up the environment for each test.

      Creates a test category.
    """
    self.category = Category.objects.create(category_name='Test category', slug='test-category')


  def test_category_creation(self):
    """
      Test if a category is created successfully.

      Asserts that the category is an instance of the Category model.
    """
    self.assertTrue(isinstance(self.category, Category))
    self.assertEqual(str(self.category), 'Test category')


  def test_category_url(self):
    """
      Test the get_url method of the Category model.

      Asserts that the generated URL matches the expected URL.
    """
    expected_url = '/store/category/test-category/'
    self.assertEqual(self.category.get_url(), expected_url)


  def test_category_has_name(self):
    """
      Test if the category has the correct name.

      Asserts that the category's name matches the expected name.
    """
    self.assertEqual(self.category.category_name, 'Test category')


  def test_category_has_slug(self):
    """
      Test if the category has the correct slug.

      Asserts that the category's slug matches the expected slug.
    """
    self.assertEqual(self.category.slug, 'test-category')


  def test_category_has_description(self):
    """
      Test if the category has an empty description by default.

      Asserts that the category's description is an empty string by default.
    """
    self.assertEqual(self.category.description, '')


  def test_category_has_image(self):
    """
      Test if the category has an empty image by default.

      Asserts that the category's image is an empty string by default.
    """
    self.assertEqual(self.category.cat_image, '')


  def test_category_has_gender(self):
    """
      Test if the category has an empty gender by default.

      Asserts that the category's gender is an empty string by default.
    """
    self.assertEqual(self.category.gender, '')


  def test_category_has_product_type(self):
    """
      Test if the category has an empty product type by default.

      Asserts that the category's product type is an empty string by default.
    """
    self.assertEqual(self.category.product_type, '')


  def test_category_str(self):
    """
      Test the __str__ method of the Category model.

      Asserts that the string representation of the category matches the category's name.
    """
    self.assertEqual(str(self.category), 'Test category')


  def test_category_get_url(self):
    """
      Test the get_url method of the Category model.

      Asserts that the generated URL matches the expected URL using reverse.
    """
    expected_url = reverse('products_by_category', args=[self.category.slug])
    self.assertEqual(self.category.get_url(), expected_url)


  def test_category_online_default_value(self):
    """
      Test if the category has an empty category_online by default.

      Asserts that the category's category_online is an empty string by default.
    """
    self.assertEqual(self.category.category_online, '')


  def test_category_description_blank(self):
    """
      Test if a category's description can be blank.

      Creates a category with an empty description and asserts that the description is empty.
    """
    category = Category.objects.create(category_name='Empty category', slug='empty-category', description='')
    self.assertEqual(category.description, '')


  def test_category_gender_choices(self):
    """
      Test the gender choices for a category.

      Creates a category with a valid gender value and asserts that it is valid.
    """
    valid_gender_category = Category()
    valid_gender_category.category_name = 'Valid gender'
    valid_gender_category.slug = 'valid-gender'
    valid_gender_category.gender = 'H'
    valid_gender_category.category_online = 'Online'
    valid_gender_category.product_type = 'A'
    valid_gender_category.clean_fields()


  def test_category_product_type_choices(self):
    """
      Test the product type choices for a category.

      Creates a category with a valid product type value and asserts that it is valid.
    """
    valid_product_type_category = Category()
    valid_product_type_category.category_name = 'Valid product type'
    valid_product_type_category.slug = 'valid-product-type'
    valid_product_type_category.gender = 'H'
    valid_product_type_category.product_type = 'A'
    valid_product_type_category.category_online = 'Online'
    valid_product_type_category.clean_fields()


  def test_category_description_max_length(self):
    """
      Test the maximum length of a category's description.

      Creates a category with a description of maximum length and asserts that its length matches the maximum length.
    """
    max_length = Category._meta.get_field('description').max_length
    category = Category.objects.create(
        category_name='Max length description',
        slug='max-length-description',
        description='a' * max_length
    )
    self.assertEqual(len(category.description), max_length)


  def test_category_image_upload(self):
    """
      Test uploading an image for a category.

      Creates a category with an image path and asserts that the image path is included in the category's cat_image path.
    """
    image_path = 'path/to/image.jpg'
    category = Category.objects.create(
        category_name='Image upload',
        slug='image-upload',
        cat_image=image_path
    )
    expected_filename = os.path.basename(image_path)
    self.assertIn(expected_filename, category.cat_image.path)
