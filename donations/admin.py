# # donations/admin.py 

# from django.contrib import admin
# from .models import Donation

# class DonationAdmin(admin.ModelAdmin):
#     list_display = ('id','donor','payment_type','donation_date','amount')
#     list_display_links = ('id','donor')
#     list_filter = 'payment_type',
#     list_editable = 'amount',
#     search_fields = 'donor',
#     list_per_page = 20

# admin.site.register(Donation,DonationAdmin)
