from django.contrib.contenttypes.models import ContentType
from django import template
from django.core.urlresolvers import reverse
register = template.Library()


@register.simple_tag
def edit_link(obj):
    edit_obj = ContentType.objects.get_for_model(obj)
    return reverse('admin:{}_{}_change'.format(edit_obj.app_label,
                                               edit_obj.model), args=(obj.id,))
