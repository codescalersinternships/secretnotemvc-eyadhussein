from django.urls import path

from . import views

app_name = "notes"
urlpatterns = [
    path("", views.list_notes_view, name="list_notes"),
    path("create/", views.create_note_view, name="create_note"),
    path("<uuid:pk>/", views.note_detail_view, name="note_detail"),
]
