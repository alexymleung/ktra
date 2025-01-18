# events/admin.py 

from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','event_type','title','publish_date')
    list_display_links = ('id','title')
    list_filter = 'event_type',
    search_fields = 'title','content'
    list_per_page = 20

admin.site.register(Event,EventAdmin)
