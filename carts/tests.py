from django.test import TestCase
from django.contrib.auth.models import User
from carts.models import Cart, CartItem
from store.models import Product
from category.models import Category
from datetime import date
from django.utils import timezone


class CartModelTest(TestCase):
  """
    Test class for the Cart model.

    Methods:
      setUpTestData: Set up initial data for the test class.
      setUp: Set up environment for each test.
      test_cart_creation: Test if a cart is created successfully.
      test_cart_str: Test the __str__ method of the Cart model.
      test_cart_item_creation: Test if a cart item is created successfully.
      test_cart_item_str: Test the __str__ method of the CartItem model.
      test_cart_item_sub_total: Test the sub_total method of the CartItem model.
      test_cart_item_is_active: Test if a cart item is active.
      test_cart_has_date_added: Test if a cart has a date_added value.
      test_cart_date_added_is_auto_now_add: Test if the date_added field of the cart is set to the current date.
      test_product_category: Test if the category of a product is correct.
      test_product_price: Test if the price of a product is correct.
      test_product_str: Test the __str__ method of the Product model.
      test_cart_item_deletion: Test if deleting a cart item reduces the total count of cart items.
      test_cart_item_update: Test if updating the quantity of a cart item reflects the change.
      test_cart_total_amount: Test if the total amount of the cart is correct.
      test_cart_item_quantity_increase: Test if increasing the quantity of a cart item reflects the change.
      test_cart_item_quantity_decrease: Test if decreasing the quantity of a cart item reflects the change.
      test_cart_item_multiple_products: Test if adding multiple products to the cart creates multiple cart items.
      test_cart_item_product_removal: Test if removing a cart item reduces the total count of cart items.
  """
  @classmethod
  def setUpTestData(cls):
    """
      Set up initial data for the test class.

      Creates a test category and a test product under the category.
    """
    test_category = Category.objects.create(category_name='test category', slug='test-category')
    Product.objects.create(product_name='Test product', price=10, category=test_category)


  def setUp(self):
    """
      Set up environment for each test.

      Creates a test cart, retrieves the test product, and creates a cart item for the product in the cart.
    """
    self.cart = Cart.objects.create(cart_id='1234')
    self.product = Product.objects.get(id=1)
    self.cart_item = CartItem.objects.create(product=self.product, cart=self.cart, quantity=1)


  def test_cart_creation(self):
    """
      Test if a cart is created successfully.

      Asserts that the cart is an instance of the Cart model.
    """
    self.assertTrue(isinstance(self.cart, Cart))


  def test_cart_str(self):
    """
      Test the __str__ method of the Cart model.

      Asserts that the string representation of the cart matches the cart_id.
    """
    self.assertEqual(str(self.cart), self.cart.cart_id)


  def test_cart_item_creation(self):
    """
      Test if a cart item is created successfully.

      Asserts that the cart item is an instance of the CartItem model.
    """
    self.assertTrue(isinstance(self.cart_item, CartItem))


  def test_cart_item_str(self):
    """
      Test the __str__ method of the CartItem model.

      Asserts that the string representation of the cart item matches the product name.
    """
    self.assertEqual(str(self.cart_item), str(self.cart_item.product))


  def test_cart_item_sub_total(self):
    """
      Test the sub_total method of the CartItem model.

      Asserts that the sub total of the cart item matches the product price multiplied by the quantity.
    """
    self.assertEqual(self.cart_item.sub_total(), self.cart_item.product.price * self.cart_item.quantity)


  def test_cart_item_is_active(self):
    """
      Test if a cart item is active.

      Asserts that the cart item is active.
    """
    self.assertTrue(self.cart_item.is_active)


  def test_cart_has_date_added(self):
    """
      Test if a cart has a date_added value.

      Asserts that the cart has a non-null date_added.
    """
    self.assertIsNotNone(self.cart.date_added)


  def test_cart_date_added_is_auto_now_add(self):
    """
      Test if the date_added field of the cart is set to the current date.

      Asserts that the date_added field of the cart matches the current date.
    """
    self.assertEqual(self.cart.date_added, date.today())


  def test_product_category(self):
    """
      Test if the category of a product is correct.

      Asserts that the category of the product matches the test category.
    """
    self.assertEqual(self.product.category.category_name, 'test category')


  def test_product_price(self):
    """
      Test if the price of a product is correct.

      Asserts that the price of the product matches the expected value.
    """
    self.assertEqual(self.product.price, 10)


  def test_product_str(self):
    """
      Test the __str__ method of the Product model.

      Asserts that the string representation of the product matches the product name.
    """
    self.assertEqual(str(self.product), self.product.product_name)


  def test_cart_item_deletion(self):
    """
      Test the deletion of a cart item.

      Asserts that deleting the cart item reduces the total count of cart items.
    """
    initial_cart_item_count = CartItem.objects.count()
    self.cart_item.delete()
    final_cart_item_count = CartItem.objects.count()
    self.assertEqual(final_cart_item_count, initial_cart_item_count - 1)


  def test_cart_item_update(self):
    """
      Test the update of a cart item's quantity.

      Updates the quantity of the cart item to a new value and asserts that it is updated correctly.
    """
    new_quantity = 5
    self.cart_item.quantity = new_quantity
    self.cart_item.save()
    updated_cart_item = CartItem.objects.get(id=self.cart_item.id)
    self.assertEqual(updated_cart_item.quantity, new_quantity)


  def test_cart_total_amount(self):
    """
      Test the calculation of the cart's total amount.

      Calculates the total amount of the cart and asserts that it matches the sub total of the cart item.
    """
    total = sum(item.sub_total() for item in self.cart.cartitem_set.all())
    self.assertEqual(total, self.cart_item.sub_total())


  def test_cart_item_quantity_increase(self):
    """
      Test increasing the quantity of a cart item.

      Increases the quantity of the cart item by 1 and asserts that it is updated correctly.
    """
    new_quantity = self.cart_item.quantity + 1
    self.cart_item.quantity = new_quantity
    self.cart_item.save()
    updated_cart_item = CartItem.objects.get(id=self.cart_item.id)
    self.assertEqual(updated_cart_item.quantity, new_quantity)


  def test_cart_item_quantity_decrease(self):
    """
      Test decreasing the quantity of a cart item.

      Decreases the quantity of the cart item by 1 (if it is greater than 1) and asserts that it is updated correctly.
    """
    if self.cart_item.quantity > 1:
      new_quantity = self.cart_item.quantity - 1
      self.cart_item.quantity = new_quantity
      self.cart_item.save()
      updated_cart_item = CartItem.objects.get(id=self.cart_item.id)
      self.assertEqual(updated_cart_item.quantity, new_quantity)


  def test_cart_item_multiple_products(self):
    """
      Test adding multiple products to the cart.

      Creates a second product and adds it to the cart, then asserts that the count of cart items is 2.
    """
    second_product = Product.objects.create(product_name='Second test product', price=15, category=self.product.category, slug='second-test-product')
    CartItem.objects.create(product=second_product, cart=self.cart, quantity=2)
    self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 2)


  def test_cart_item_product_removal(self):
    """
      Test removing a product from the cart.

      Deletes the cart item and asserts that the count of cart items is reduced by 1.
    """
    initial_cart_item_count = CartItem.objects.filter(cart=self.cart).count()
    self.cart_item.delete()
    final_cart_item_count = CartItem.objects.filter(cart=self.cart).count()
    self.assertEqual(final_cart_item_count, initial_cart_item_count - 1)
