from django import template

from notes.models import Label

register = template.Library()


@register.inclusion_tag('notes/label_list_nav.html')
def label_list_nav(request, user):
    curr_label = request.GET.get('label')
    return {
        'labels': Label.objects.all().filter(user__username=user),
        'curr_label': curr_label
    }
