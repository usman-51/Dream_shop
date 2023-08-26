from django.test import TestCase, Client
from django.urls import reverse
from .models import Account
from .forms import RegistrationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required


class AccountModelTest(TestCase):
  """
    Test class for the Account model.

    Methods:
      setUp: Set up environment for each test.
      test_account_creation: Test if a user account is created successfully.
      test_account_str: Test the __str__ method of the Account model.
  """
  def setUp(self):
    """
      Set up environment for each test.

      Creates a new user account.
    """
    self.account1 = Account.objects.create_user(first_name='test', last_name='user', email='test#user.com', username='testuser', password='password')
  

  def test_account_creation(self):
    """
      Test if a user account is created successfully.

      Asserts that the count of Account objects is 1.
    """
    self.assertEqual(Account.objects.count(), 1)


  def test_account_str(self):
    """
      Test the __str__ method of the Account model.

      Asserts that the string representation of the account is the email of the user.
    """
    self.assertEqual(str(self.account1), 'test#user.com') 



class RegistrationFormTest(TestCase):
  """
    Test class for the RegistrationForm form.

    Methods:
      test_form_validity: Test if the RegistrationForm is valid with correct data.
  """
  def test_form_validity(self):
    """
      Test if the RegistrationForm is valid with correct data.

      Asserts that the form is valid.
    """
    form = RegistrationForm(data={
      'civility': 'M',
      'first_name': 'test',
      'last_name': 'user',
      'address': '123 street',
      'postal_code': '12345',
      'city': 'test city',
      'country': 'test country',
      'email': 'test@user.com',
      'phone_number': '1234567890',
      'birth_date': '01/01/2000',
      'password': 'Password123!',
      'confirm_password': 'Password123!'
    })
    self.assertTrue(form.is_valid())



class AccountViewTest(TestCase):
  """
    Test class for the views of the accounts application.

    Methods:
      setUp: Set up environment for each test.
      test_register_view: Test if the register view works correctly with correct data.
      test_login_view: Test if the login view works correctly with valid credentials.
      test_logout_view: Test if the logout view works correctly.
      test_register_view_get: Test if the register view returns a 200 status code for a GET request.
      test_login_view_get: Test if the login view returns a 200 status code for a GET request.
      test_logout_view_unauthenticated: Test if the logout view returns a 302 status code if the user is not authenticated.
      test_register_view_invalid_post: Test if the register view returns a 400 status code for an invalid POST request.
      test_login_view_invalid_post: Test if the login view returns a 302 status code for an invalid POST request.
      test_logout_view_not_found: Test if the logout view returns a 404 status code for a GET request on a non-existent URL.
      test_register_view_not_found: Test if the register view returns a 404 status code for a GET request on a non-existent URL.
      test_login_view_not_found: Test if the login view returns a 404 status code for a GET request on a non-existent URL.
      test_logout_view_authenticated: Test if the logout view returns a 302 status code if the user is authenticated.
  """
  def setUp(self):
    """
      Set up environment for each test.

      Defines the URLs and initializes a test client.
    """
    self.client = Client()
    self.register_url = reverse('register')
    self.login_url = reverse('login')
    self.logout_url = reverse('logout')


  def test_register_view(self):
    """
      Test the register view with correct data.

      Asserts that the response status code is 200.
    """
    response = self.client.post(self.register_url, {
      'civility': 'M',
      'first_name': 'test',
      'last_name': 'user',
      'address': '123 street',
      'postal_code': '12345',
      'city': 'test city',
      'country': 'test country',
      'email': 'test@user.com',
      'phone_number': '1234567890',
      'birth_date': '01/01/2000',
      'password': 'Password123!',
      'confirm_password': 'Password123!'
    }, format='json')
    self.assertEqual(response.status_code, 200)


  def test_login_view(self):
    """
      Test the login view with valid credentials.

      Asserts that the response status code is 302.
    """
    Account.objects.create_user(first_name='test', last_name='user', email='test@user.com', username='testuser', password='password')
    response = self.client.post(self.login_url, {'email': 'test@user.com', 'password': 'password'}, format='json')
    self.assertEqual(response.status_code, 302)


  def test_logout_view(self):
    """
      Test the logout view.

      Asserts that the response status code is 302 and the user is not authenticated.
    """
    Account.objects.create_user(first_name='test', last_name='user', email='test@user.com', username='testuser', password='password')
    self.client.login(email='test@user.com', password='password')
    response = self.client.get(self.logout_url)
    self.assertEqual(response.status_code, 302)
    user = auth.get_user(self.client)
    self.assertFalse(user.is_authenticated)


  def test_register_view_get(self):
    """
      Test the register view with a GET request.

      Asserts that the response status code is 200.
    """
    response = self.client.get(self.register_url)
    self.assertEqual(response.status_code, 200)


  def test_login_view_get(self):
    """
      Test the login view with a GET request.

      Asserts that the response status code is 200.
    """
    response = self.client.get(self.login_url)
    self.assertEqual(response.status_code, 200)


  def test_logout_view_unauthenticated(self):
    """
      Test the logout view with an unauthenticated user.

      Asserts that the response status code is 302.
    """
    response = self.client.get(self.logout_url)
    self.assertEqual(response.status_code, 302)


  def test_register_view_invalid_post(self):
    """
      Test the register view with an invalid POST request.

      Asserts that the response status code is 400.
    """
    response = self.client.post(self.register_url, {
      'civility': 'M',
      'first_name': 'test',
      'last_name': 'user',
      'address': '123 street',
      'postal_code': '1234',
      'city': 'test city',
      'country': 'test country',
      'email': 'invalid.com',
      'phone_number': '123456789',
      'birth_date': '01-01-2000',
      'password': 'Password123',
      'confirm_password': 'Password123'
    }, format='json')
    self.assertEqual(response.status_code, 400)


  def test_login_view_invalid_post(self):
    """
      Test the login view with an invalid POST request.

      Asserts that the response status code is 302.
    """
    response = self.client.post(self.login_url, {
      'email': 'test@user.com',
      'password': 'incorrect_password',
    }, format='json')
    self.assertEqual(response.status_code, 302)


  def test_logout_view_not_found(self):
    """
      Test the logout view with a GET request on a non-existent URL.

      Asserts that the response status code is 404.
    """
    response = self.client.get('/accounts/logout/invalid/')
    self.assertEqual(response.status_code, 404)


  def test_register_view_not_found(self):
    """
      Test the register view with a GET request on a non-existent URL.

      Asserts that the response status code is 404.
    """
    response = self.client.get('/accounts/register/invalid/')
    self.assertEqual(response.status_code, 404)


  def test_login_view_not_found(self):
    """
      Test the login view with a GET request on a non-existent URL.

      Asserts that the response status code is 404.
    """
    response = self.client.get('/accounts/login/invalid/')
    self.assertEqual(response.status_code, 404)


  def test_logout_view_authenticated(self):
    """
      Test the logout view with an authenticated user.

      Asserts that the response status code is 302.
    """
    Account.objects.create_user(
        first_name='test',
        last_name='user',
        email='test@user.com',
        username='testuser',
        password='password'
    )
    self.client.login(email='test@user.com', password='password')
    response = self.client.get(self.logout_url)
    self.assertEqual(response.status_code, 302)
