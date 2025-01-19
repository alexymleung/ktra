# events/views.py 

from django.shortcuts import render, get_object_or_404
from .models import Event
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def events(request, event_type=None):
    # Retrieve and order events by publish date
    events_queryset = Event.objects.order_by('-publish_date')

    # Filter by event_type if provided
    if event_type:
        events_queryset = events_queryset.filter(event_type__iexact=event_type)

    context = {
        'events': events_queryset,
        'event_type': event_type,
    }
    return render(request, 'events/events.html', context)

def event(request, event_id):
    event_instance = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event_instance,
        'event_type': event_instance.event_type,  # Ensure this is passed to the template
    }
    
    return render(request, 'events/event.html', context)

def get_event_type_label(key):
    event_types_dict = dict(event_type_choices)
    return event_types_dict.get(key, key)
