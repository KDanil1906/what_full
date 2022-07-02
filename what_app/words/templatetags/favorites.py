from django import template
from django.contrib.auth.models import User

from words.models import ProfileUser, Favorite

register = template.Library()


@register.simple_tag()
def favorite_words(request):

    favorite = {}
    all_favorites = Favorite.objects.all()
    user_id = ProfileUser.objects.get(name=User.objects.get(id=request.user.id))
    if all_favorites.filter(user_id=user_id).exists():
        favorite = all_favorites.filter(user_id=user_id)

    return favorite
