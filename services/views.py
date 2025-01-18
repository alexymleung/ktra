from django.shortcuts import render,get_object_or_404
from .models import Service
from bookings.models import Booking

def services(request,service_type):
    # Retrieve and order services by service date
    queryset_services = Service.objects.order_by('-service_date')
    
    # Filter by service_type if provided
    if service_type:
        queryset_services = queryset_services.filter(service_type__iexact = service_type)
    
    context = {
        'services': queryset_services,
        'service_type': service_type
    }
    return render(request,'services/services.html',context)

def service(request,service_id):
    object_service = get_object_or_404(Service,pk=service_id)
    service_bookings = Booking.objects.filter(service=object_service)
    remind_quota = object_service.quota - len(service_bookings)
    quota_range = range(1,remind_quota)
    has_remind = False
    if remind_quota > 0:
        has_remind = True
    context = {
        'service': object_service,
        'quota_range': quota_range,
        'has_remind': has_remind
    }
    return render(request,'services/service.html',context)
