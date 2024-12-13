from django import template

register = template.Library()

@register.filter
def get_role_display_safe(user):
    if user:
        return user.get_role_display()
    return "None"
