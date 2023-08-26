from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class MyAccountManager(BaseUserManager):
  """
    Custom account manager where an email is the unique identifiers
    for authentication instead of usernames.

    Methods:
      create_user: Create and save a User with the given email, username and password.
      create_superuser: Create and save a SuperUser with the given email, username and password.
  """
  def create_user(self, first_name, last_name, username, email, password=None):
    """
      Create and save a User with the given email, username and password.

      Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        username (str): Username of the user.
        email (str): Email of the user.
        password (str, optional): Password of the user. Defaults to None.
      
      Returns:
        User: The user that was created.
    """
    if not email:
      raise ValueError('User must have an email address')
    
    if not username:
      raise ValueError('User must have an username')
    
    user = self.model(
      email      = self.normalize_email(email),
      username   = username,
      first_name = first_name,
      last_name  = last_name,
    )

    user.set_password(password)
    user.save(using=self._db)

    return user
  

  def create_superuser(self, first_name, last_name, email, username, password):
    """
      Create and save a SuperUser with the given email, username and password.

      Args:
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Email of the user.
        username (str): Username of the user.
        password (str): Password of the user.
      
      Returns:
        User: The user that was created.
    """
    user = self.create_user(
      email      = self.normalize_email(email),
      username   = username,
      password   = password,
      first_name = first_name,
      last_name  = last_name,
    )
    user.is_admin      = True
    user.is_active     = True
    user.is_staff      = True
    user.is_superadmin = True
  
    user.save(using=self._db)
  
    return user


class Account(AbstractBaseUser):
  """
    Custom User model where email is the unique identifier
    and has an is_admin field to allow access to admin app

    Attributes:
      GENDER_CHOICES (tuple): Choices for the gender of the user.
      civility (CharField): The user's civility. This field uses the GENDER_CHOICES.
      first_name (CharField): The user's first name.
      last_name (CharField): The user's last name.
      address (CharField): The user's address.
      postal_code (CharField): The user's postal code.
      city (CharField): The user's city.
      country (CharField): The user's country.
      email (EmailField): The user's email.
      phone_number (CharField): The user's phone number.
      birth_date (DateField): The user's birth date.
      username (CharField): The user's username.
      date_joined (DateTimeField): The date the user joined.
      last_login (DateTimeField): The user's last login date and time.
      is_admin (BooleanField): If the user is an admin.
      is_staff (BooleanField): If the user is staff.
      is_active (BooleanField): If the user is active.
      is_superadmin (BooleanField): If the user is a superadmin.
      USERNAME_FIELD (str): The field to use as username.
      REQUIRED_FIELDS (list): The fields that are required.
      objects (MyAccountManager): The account manager for the user.
    """
  GENDER_CHOICES = (
    ('F', 'Madame'),
    ('M', 'Monsieur'),
  )

  civility        = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')
  first_name      = models.CharField(max_length=50)
  last_name       = models.CharField(max_length=50)
  address         = models.CharField(max_length=100, default='')
  postal_code     = models.CharField(max_length=20, default='00000')
  city            = models.CharField(max_length=50, default='')
  country         = models.CharField(max_length=50, default='')
  email           = models.EmailField(max_length=100, unique=True)
  phone_number    = models.CharField(max_length=50)
  birth_date      = models.DateField(default=timezone.now)
  username        = models.CharField(max_length=50, unique=True)

  date_joined     = models.DateTimeField(auto_now_add=True)
  last_login      = models.DateTimeField(auto_now_add=True)
  is_admin        = models.BooleanField(default=False)
  is_staff        = models.BooleanField(default=False)
  is_active       = models.BooleanField(default=False)
  is_superadmin   = models.BooleanField(default=False)

  # Definition of the field used as the identifier for this user model.
  USERNAME_FIELD  = 'email'
  # Required fields when creating a user:
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  # Link the user model with the previously created manager.
  objects = MyAccountManager()


  def get_civility_display(self):
    """
      Returns the readable value of the civility choice field.

      Returns:
        str: The readable value of the civility.
    """
    return dict(self.GENDER_CHOICES).get(self.civility)


  def __str__(self):
    """
      Returns the string representation of the user.

      Returns:
        str: The string representation of the user.
    """
    return self.email


  def has_perm(self, perm, obj=None):
    """
      Checks if user has a specific permission.

      Args:
        perm (str): The permission to check.
        obj (Model, optional): The object to check the permission against. Defaults to None.

      Returns:
        bool: If the user has the permission.
    """
    return self.is_admin


  def has_module_perms(self, add_label):
    """
      Checks if user has permissions to view the app `add_label` (always True for simplicity)

      Args:
        add_label (str): The label of the app.

      Returns:
        bool: If the user has the permission.
    """
    return True
