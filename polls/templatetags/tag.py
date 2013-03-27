from django import template
from django.template import RequestContext, Context
import re

register = template.Library()


@register.simple_tag
def active(path, pattern):
	if re.search(pattern, path):
		return 'active'
	return ''  


