from django import template

register = template.Library()

@register.simple_tag
def previous_page_range(page_obj):
    pass

@register.simple_tag
def next_page_range(page_obj):
    pass
