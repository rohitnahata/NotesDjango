from rest_framework.generics import ListAPIView
from notes.models import Note


class NoteListAPIView(ListAPIView):
    queryset = Note.objects.all()
