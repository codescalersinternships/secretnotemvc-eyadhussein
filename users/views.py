"""Users module contains views for user registration, login, and logout. """

from django.shortcuts import render, redirect
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm


@ratelimit(key="ip", rate="50/h", block=True)
def register_view(request):
    """
    Handle user registration.

    - If the request method is POST, validate and save the registration form.
    - If the form is valid, create a new user and log them in.
    - Redirect to the note creation view on successful registration.
    - If the request method is GET, render an empty registration form.

    This view is rate-limited to 50 requests per hour per IP address.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered template with the registration form or a redirect to the note creation view.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("notes:create_note"))
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


@ratelimit(key="ip", rate="50/h", block=True)
def login_view(request):
    """
    Handle user login.

    - If the request method is POST, validate and authenticate the login form.
    - If the form is valid and the user credentials are correct, log the user in.
    - Redirect to the note list view on successful login.
    - If the request method is GET, render an empty login form.

    This view is rate-limited to 50 requests per hour per IP address.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered template with the login form or a redirect to the note list view.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("notes:list_notes"))
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Handle user logout.

    - Log out the currently authenticated user.
    - Redirect to the login view.

    This view requires the user to be authenticated.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: A redirect to the login view.
    """
    logout(request)
    return redirect(reverse("users:login"))
