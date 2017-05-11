from django.forms import ModelForm

from .models import Note, Label


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['note_title', 'note_text', 'labels', 'public', 'archived', 'pinned']


class NoteArchiveForm(ModelForm):
    class Meta:
        model = Note
        fields = ['archived']


class LabelForm(ModelForm):
    class Meta:
        model = Label
        exclude = ('author',)
