from django import template
from events.choices import event_type_choices, service_type_choices
from datetime import datetime, timezone

register = template.Library()

@register.filter
def get_event_label(key):
    event_types_dict = dict(event_type_choices)
    return event_types_dict.get(key, key)

@register.filter
def get_service_label(key):
    service_types_dict = dict(service_type_choices)
    return service_types_dict.get(key, key)

@register.filter
def chinese_date(value):
    if not value:
        return ''
    
    return f'{value.year}年{value.month}月{value.day}日' 