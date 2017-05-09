from django.forms import ModelForm

from .models import Note, Label


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['note_title', 'note_text', 'labels', 'public']


class LabelForm(ModelForm):
    class Meta:
        model = Label
        exclude = ('user',)
