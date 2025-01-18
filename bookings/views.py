from django.shortcuts import redirect
from django.contrib import messages
from bookings.models import Booking

def booking(request):
    if request.method == 'POST':
        service_id = request.POST['service_id']
        service_quota = request.POST['service_quota']
        if request.user.is_authenticated:
            user_id = request.user.id
        for i in range(1,int(service_quota)+1):
            booking = Booking(
                            service_id=service_id,
                            user_id=user_id
                            )
            booking.save()
        messages.success(request,"你已成功預約")
    return redirect("/services/"+service_id)
    