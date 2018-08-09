import re
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def extract_name(html_name):
    l = html_name.split('-')
    return " ".join([l[val] for val in range(len(l)-1)])
