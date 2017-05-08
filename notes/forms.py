from django.forms import ModelForm, ImageField

from .models import Note, Images


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['note_title', 'note_text', 'labels', 'public']


class ImageForm(ModelForm):
    image = ImageField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)
