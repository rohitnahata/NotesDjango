from django.forms import ModelForm
from .models import Note


class NoteForm(ModelForm):

    class Meta:
        model = Note
        fields = ['note_title', 'note_text', 'labels', 'public']
