from django.shortcuts import redirect,get_object_or_404
from django.contrib import messages
# from django.core.mail import send_mail
from bookings.models import Booking

def booking(request):
    if request.method == 'POST':
        service_id = request.POST['service_id']
        if request.user.is_authenticated:
            user_id = request.user.id
        booking = Booking(
                        service_id=service_id,
                        user_id=user_id
                        )
        booking.save()
        # send_mail(
        #     "Listing Inquiry",
        #     "Inquiry for "+listing_title+". Sign into admin for more info",
        #     "admin@bcre.com",
        #     [realtor_email,"kim29112024@gmail.com"],
        #     fail_silently=False
        # )
        messages.success(request,"You have been sign up.")
    return redirect("/services/"+service_id)
    