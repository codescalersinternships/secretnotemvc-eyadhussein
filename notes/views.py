"""Notes module contains the views for the notes app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotFound
from django_ratelimit.decorators import ratelimit
from .models import Note
from .forms import NoteForm


@login_required
@ratelimit(key="ip", rate="50/h", block=True)
def create_note_view(request):
    """
    Handle the creation of a new note.

    - If the request method is POST, validate and save the note form.
    - If the form is valid, associate the note with the current user and save it.
    - Redirect to the notes list view on successful creation.
    - If the request method is GET, render an empty note form.

    This view is rate-limited to 50 requests per hour per IP address.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered template with the note form.
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            note = form.save()
            return redirect(reverse("notes:list_notes"), pk=note.id)
    else:
        form = NoteForm()
    return render(request, "notes/create_note.html", {"form": form})


@login_required
def list_notes_view(request):
    """
    Display a list of notes created by the authenticated user.

    - Retrieve all notes associated with the current user.
    - Render the notes list template with the retrieved notes.

    This view requires the user to be authenticated.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The rendered template with the list of notes.
    """
    notes = Note.objects.filter(user=request.user)
    return render(request, "notes/list_notes.html", {"notes": notes})


@ratelimit(key="ip", rate="50/h", block=True, method="GET")
def note_detail_view(request, pk):
    """
    Display the details of a specific note.

    - Retrieve the note by its primary key (pk).
    - If the note is expired or has reached the maximum number of views, delete it and return a 404 response.
    - Increment the current views of the note and save it.
    - If the note becomes expired after incrementing the views, delete it.
    - Render the note detail template with the note details.

    This view is rate-limited to 50 requests per hour per IP address for GET requests.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - pk (str): The primary key of the note.

    Returns:
    - HttpResponse: The rendered template with the note details or a 404 response if the note is expired or deleted.
    """
    note = get_object_or_404(Note, pk=pk)
    if note.is_expired():
        note.delete()
        return HttpResponseNotFound(
            "this note has expired or been viewed the maximum number of times"
        )
    note.current_views += 1
    note.save()
    if note.is_expired():
        note.delete()
    return render(request, "notes/note_detail.html", {"note": note})
