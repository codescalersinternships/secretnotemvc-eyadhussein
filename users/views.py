from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm


# Create your views here.
@ratelimit(key="ip", rate="50/h", block=True)
def register_view(request):
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
    logout(request)
    return redirect(reverse("users:login"))
