from django import template
from django.contrib.auth.models import Group
from ..models import UserInfo

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()

@register.filter(name='info')
def info(user):
    return UserInfo.get(user)