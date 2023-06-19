from django import template

register = template.Library()

@register.filter
def filter_none_stacks(stacks):
    return [stack for stack in stacks if stack.name is not None]
