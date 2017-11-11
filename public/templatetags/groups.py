from django import template
from ..models import Member, Server
import random

register = template.Library()

@register.assignment_tag(name='staff_check')
def staff_check(user, server_id):
    if user.is_authenticated:
        server = Server.get(server_id)
        mem = Member.getMember(user=user, server=server)
        if mem:
            return mem.staff
    return False


@register.assignment_tag(name='false')
def false():
    return False


@register.assignment_tag(name='random_pic')
def random_pic():
    option_count = 5
    option = random.randint(1, option_count)
    result = "public/random/" + str(option) + ".jpg"
    return result