from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Note


# Create your tests here.
class NoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.note = Note.objects.create(
            user=self.user,
            title="Test Note",
            content="This is a test note",
            expiration_date=timezone.now() + timedelta(days=30),
            max_views=3,
        )

    def test_is_expired_by_date(self):
        self.assertFalse(self.note.is_expired())
        self.note.expiration_date = timezone.now() - timedelta(days=1)
        self.note.save()
        self.assertTrue(self.note.is_expired())

    def test_is_expired_by_views(self):
        self.assertFalse(self.note.is_expired())
        self.note.current_views = self.note.max_views
        self.note.save()
        self.assertTrue(self.note.is_expired())

    def test_is_not_expired(self):
        self.note.expiration_date = timezone.now() + timedelta(days=1)
        self.note.current_views = self.note.max_views - 1
        self.note.save()
        self.assertFalse(self.note.is_expired())


class CreateNoteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.create_url = reverse("notes:create_note")

    def test_create_note_view_get(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/create_note.html")

    def test_create_note_view_post(self):
        self.client.login(username="testuser", password="12345")
        timezone_test = timezone.now() + timedelta(days=30)
        data = {
            "title": "New Test Note",
            "content": "This is a new test note",
            "expiration_date": timezone_test,
            "max_views": 5,
            "current_views": 0,
            "user": self.user,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="New Test Note").exists())

        created_note = Note.objects.get(title="New Test Note")

        self.assertEqual(created_note.title, "New Test Note")
        self.assertEqual(created_note.content, "This is a new test note")
        self.assertEqual(created_note.expiration_date.date(), timezone_test.date())
        self.assertEqual(created_note.max_views, 5)
        self.assertEqual(created_note.current_views, 0)
        self.assertEqual(created_note.user, self.user)

    def test_login_required_for_create_note(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.client.logout()


class ListNotesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.list_url = reverse("notes:list_notes")

    def test_list_notes_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/list_notes.html")

    def test_login_required_for_list_notes(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.client.logout()


class NoteDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.note = Note.objects.create(
            user=self.user,
            title="Test Note",
            content="This is a test note",
            expiration_date=timezone.now() + timedelta(days=30),
            max_views=3,
        )
        self.detail_url = reverse("notes:note_detail", kwargs={"pk": self.note.pk})

    def test_note_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notes/note_detail.html")
        self.assertContains(response, "Test Note")

    def test_note_detail_view_expired_by_date(self):
        self.note.expiration_date = timezone.now() - timedelta(days=1)
        self.note.save()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "this note has expired", status_code=404)

    def test_note_detail_view_expired_by_views(self):
        self.note.current_views = self.note.max_views
        self.note.save()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "this note has expired", status_code=404)

    def test_note_detail_view_increment_views(self):
        initial_views = self.note.current_views
        response = self.client.get(self.detail_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.current_views, initial_views + 1)

    def tearDown(self):
        self.client.logout()


class EndToEndTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")
        self.create_note_url = reverse("notes:create_note")
        self.list_notes_url = reverse("notes:list_notes")

        self.user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "*Newpassword1234#",
            "password2": "*Newpassword1234#",
        }

        self.note_data = {
            "title": "E2E Test Note",
            "content": "This is a test note created during E2E test.",
            "expiration_date": timezone.now() + timedelta(days=30),
            "max_views": 5,
        }

    def test_user_registration_and_login_and_create_note_flow(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

        login_data = {
            "username": "newuser",
            "password": "*Newpassword1234#",
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.list_notes_url))

        response = self.client.post(self.create_note_url, self.note_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title="E2E Test Note").exists())

        response = self.client.get(self.list_notes_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("E2E Test Note", response.content.decode())

    def tearDown(self):
        self.client.logout()
