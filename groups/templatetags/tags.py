from django import template
from wishlist.models import Wish

register = template.Library()

@register.simple_tag
def get_wishlist_existence(group, user):
    if (len(Wish.objects.filter(group=group).filter(author=user)) > 0):
        result = "Yes"
    else:
        result = "No"
    return result