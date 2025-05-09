from django import template
from jalali_date import datetime2jalali

register = template.Library()

@register.filter
def to_jalali(value):
    if value:
        return datetime2jalali(value).strftime('%Y/%m/%d _ %H:%M')
    return ""
