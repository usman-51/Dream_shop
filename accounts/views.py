from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def register(request):
  """
    Manages the registration of a new user.

    If the request method is POST, this function retrieves the registration form data from the request,
    then validates the form. If the form is valid, a new user is created and saved in the database,
    a success message is displayed to the user, and a JSON response indicating success is returned.
    If the form is not valid, a JSON response indicating failure and containing the form errors is returned.

    If the request method is not POST (e.g., GET), this function creates a new empty registration form
    and returns the registration page with this form.
    
    Args:
    request (HttpRequest): The received HTTP request.
    
    Returns:
    HttpResponse: The HTTP response to be sent back to the client.
  """
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      civility         = form.cleaned_data['civility']
      first_name       = form.cleaned_data['first_name']
      last_name        = form.cleaned_data['last_name']
      address          = form.cleaned_data['address']
      postal_code      = form.cleaned_data['postal_code']
      city             = form.cleaned_data['city']
      country          = form.cleaned_data['country']
      email            = form.cleaned_data['email']
      phone_number     = form.cleaned_data['phone_number']
      birth_date       = form.cleaned_data['birth_date']
      password         = form.cleaned_data['password']
      confirm_password = form.cleaned_data['confirm_password']
      username         = email.split("@")[0]

      user = Account.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        username=username,
        password=password,
      )
      user.phone_number = phone_number
      user.address = address
      user.postal_code = postal_code
      user.birth_date = birth_date
      user.city = city
      user.country = country
      user.civility = civility
      user.save()
      messages.success(request, 'Inscription confirmée.')
      return JsonResponse({'success': True})
    else:
      errors = form.errors.as_json()
      return JsonResponse({'success': False, 'errors': errors}, status=400)
  else:
    form = RegistrationForm()


  context = {
    'form': form,
  }
  return render(request, 'accounts/register.html', context)


def login(request):
  """
    Manages the login of a user.

    If the request method is POST, this function retrieves the user's email and password from the request,
    then attempts to authenticate the user. If the user is successfully authenticated, they are logged in and redirected to the home page.
    Otherwise, an error message is displayed to the user and they are redirected to the login page.
    
    If the request method is not POST (e.g., GET), this function simply returns the login page.
    
    Args:
    request (HttpRequest): The received HTTP request.
    
    Returns:
    HttpResponse: The HTTP response to be sent back to the client.
  """
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)

    if user is not None:
      auth.login(request, user)
      #messages.success(request, "Vous êtes bien connecté !")
      return redirect('home')
    else:
      messages.error(request, "Identification échouée, veuillez vérifier vos identifiants !")
      return redirect('login')

  return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
  """
    Manages the logout of a user.
    
    This function logs out the user, displays a success message,
    and redirects the user to the login page.
    
    This function requires the user to be logged in (determined by the login_required decorator).
    
    Args:
    request (HttpRequest): The received HTTP request.
    
    Returns:
    HttpResponse: The HTTP response to be sent back to the client.
  """
  auth.logout(request)
  messages.success(request, 'Vous êtes bien déconnecté !')
  return redirect('login')
