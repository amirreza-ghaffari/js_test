from django import template
register = template.Library()


@register.filter
def replace_active(value):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if value == 'is_active':
        return value.replace('is_active', 'فعال شده')
    if value == 'is_approved':
        return value.replace('is_approved', 'تایید شده')
    return value


@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)


@register.filter
def upper_case(value):
    value = value.replace('_', ' ')
    return value.title()



