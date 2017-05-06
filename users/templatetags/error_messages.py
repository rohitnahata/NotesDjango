from django import template
register = template.Library()


@register.inclusion_tag('registration/error_messages.html')
def error_messages(errors):
    return {'errors': errors}
