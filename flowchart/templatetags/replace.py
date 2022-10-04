from django import template
register = template.Library()


@register.filter
def replace(value):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if value == 'is_active':
        return value.replace('is_active', 'فعال شده')
    if value == 'is_approved':
        return value.replace('is_approved', 'تایید شده')
    return value
