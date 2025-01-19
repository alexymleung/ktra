# events/views.py
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone  # Importing timezone for now()
from events.choices import event_type_choices, publish_date_choices

def events(request, event_type=None):
    # Retrieve and order events by publish date
    events_queryset = Event.objects.order_by('-publish_date')

    # Filter by event_type if provided
    if event_type:
        events_queryset = events_queryset.filter(event_type__iexact=event_type)

    context = {
        'publish_date_choices': publish_date_choices,
        'event_type_choices': event_type_choices,
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

def search(request):
    queryset_list = Event.objects.order_by('-publish_date')
    
    # Filter by keywords in content
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(content__icontains=keywords)
    
    # Filter by title
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            queryset_list = queryset_list.filter(title__icontains=title)

    # Filter by publish_date
    if 'publish_date' in request.GET:
        publish_date = request.GET['publish_date']
        if publish_date:
            if publish_date != '_':
                # Convert the selection to an integer and filter accordingly
                days_ago = int(publish_date)  # Convert string to integer
                queryset_list = queryset_list.filter(publish_date__gte=timezone.now() - timezone.timedelta(days=days_ago))

    # Filter by event_type
    if 'event_type' in request.GET:
        event_type = request.GET['event_type']
        if event_type and event_type != '_':
            queryset_list = queryset_list.filter(event_type__iexact=event_type)

    paginator = Paginator(queryset_list, 3)
    page = request.GET.get("page")
    paged_listings = paginator.get_page(page)
    
    context = {
        'publish_date_choices': publish_date_choices,
        'event_type_choices': event_type_choices,  # Pass event type choices to the template
        'events': paged_listings,
        'values': request.GET
    }
    return render(request, 'events/search.html', context)