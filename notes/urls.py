from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    path("", views.list_notes_view, name="list_notes"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("create/", views.create_note_view, name="create_note"),
    path("note/<uuid:pk>/", views.note_detail_view, name="note_detail"),
]
