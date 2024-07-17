from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("users:register")

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_view_post(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "*Testpassword1234#",
            "password2": "*Testpassword1234#",
        }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_view_invalid_post(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "differentpassword",
        }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="testuser").exists())


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("users:login")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        form = LoginForm(request="POST", data=data)
        self.assertTrue(form.is_valid())

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse("notes:list_notes"))

    def test_login_view_invalid_post(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword",
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("users:logout")
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse("users:login"))

    def test_logout_view_unauthenticated(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url, reverse("users:login"))
