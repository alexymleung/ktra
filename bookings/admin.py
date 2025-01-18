from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','service_id')
    list_display_links = ('id',)
    list_per_page = 20

admin.site.register(Booking,BookingAdmin)