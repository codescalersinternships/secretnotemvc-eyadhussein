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
    notes = Note.objects.filter(user=request.user)
    return render(request, "notes/list_notes.html", {"notes": notes})


@ratelimit(key="ip", rate="50/h", block=True, method="GET")
def note_detail_view(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if note.is_expired():
        note.delete()
        return HttpResponseNotFound(
            "this note has expired or been viewed the maximum number of times."
        )
    note.current_views += 1
    note.save()
    if note.is_expired():
        note.delete()
    return render(request, "notes/note_detail.html", {"note": note})
