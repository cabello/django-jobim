from django import template

from jobim.models import Category


register = template.Library()


@register.inclusion_tag('jobim/categories_list.html')
def categories_list():
    categories = Category.objects.all()
    return {'categories': categories}
