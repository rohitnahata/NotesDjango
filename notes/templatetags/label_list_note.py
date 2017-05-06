from django import template

from notes.models import Label

register = template.Library()


@register.inclusion_tag('notes/label_list_note.html')
def label_list_note(labels):
    labels = labels or Label.objects.all()
    return {'labels': labels}
