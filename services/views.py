# services/views.py
from django.shortcuts import render,get_object_or_404
from .models import Service
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from bookings.models import Booking
from django.utils import timezone  # Importing timezone for now()
from services.choices import service_type_choices, service_date_choices

def services(request,service_type):
    # Retrieve and order services by service date
    queryset_services = Service.objects.order_by('-service_date')
    
    # Filter by service_type if provided
    if service_type:
        queryset_services = queryset_services.filter(service_type__iexact = service_type)
    
    for sobj in queryset_services:
        service_bookings = Booking.objects.filter(service=sobj)
        remind_quota = sobj.quota - len(service_bookings)
        if remind_quota<1:
            sobj.no_remind = True
    context = {
        'service_date_choices': service_date_choices,
        'service_type_choices': service_type_choices,
        'services': queryset_services,
        'service_type': service_type
    }
    return render(request,'services/services.html',context)

def service(request,service_id):
    object_service = get_object_or_404(Service,pk=service_id)
    service_bookings = Booking.objects.filter(service=object_service)
    remind_quota = object_service.quota - len(service_bookings)
    quota_range = range(1,remind_quota+1)
    has_remind = False
    if remind_quota > 0:
        has_remind = True
    context = {
        'service': object_service,
        'quota_range': quota_range,
        'has_remind': has_remind
    }
    return render(request,'services/service.html',context)

def search(request):
    queryset_list = Service.objects.order_by('-service_date')
    
    # Filter by keywords in content
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    # Filter by title
    if 'title' in request.GET:
        title = request.GET['title']
        if title:
            queryset_list = queryset_list.filter(title__icontains=title)

    # Filter by publish_date
    if 'service_date' in request.GET:
        service_date = request.GET['service_date']
        if service_date:
            if service_date != '_':
                # Convert the selection to an integer and filter accordingly
                days_ago = int(service_date)  # Convert string to integer
                queryset_list = queryset_list.filter(service_date__lte=timezone.now() + timezone.timedelta(days=days_ago))

    # Filter by event_type
    if 'service_type' in request.GET:
        service_type = request.GET['service_type']
        if service_type and service_type != '_':
            queryset_list = queryset_list.filter(service_type__iexact=service_type)

    paginator = Paginator(queryset_list, 3)
    page = request.GET.get("page")
    paged_listings = paginator.get_page(page)
    
    context = {
        'service_date_choices': service_date_choices,
        'service_type_choices': service_type_choices,  # Pass event type choices to the template
        'services': paged_listings,
        'values': request.GET
    }
    return render(request, 'services/search.html', context)
