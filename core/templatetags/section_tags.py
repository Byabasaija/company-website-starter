from django import template
from django.template.loader import get_template
from django.template.exceptions import TemplateDoesNotExist
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def render_section(context, section_type, variant='default'):
    variant = variant or 'default'
    primary  = f'components/sections/{section_type}/{variant}.html'
    fallback = f'components/sections/{section_type}/default.html'

    for path in (primary, fallback):
        try:
            t = get_template(path)
            return mark_safe(t.render(context.flatten()))
        except TemplateDoesNotExist:
            continue

    return ''
