from django import template

register = template.Library()


#================function to filter links by category===================
@register.filter()
def in_category(links, category):
    return links.filter(category=category)
