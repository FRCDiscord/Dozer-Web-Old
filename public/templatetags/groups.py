from django import template
from ..models import Member, Server

register = template.Library()

@register.assignment_tag(name='staff_check')
def staff_check(user, server_id):
    server = Server.get(server_id)
    mem = Member.getMember(user=user, server=server)
    if mem:
        return mem.staff
    else:
        return False


@register.assignment_tag(name='false')
def false():
    return False