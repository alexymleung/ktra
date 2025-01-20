from django.contrib import admin
from .models import IndexImage, GeneralInformation

class IndexImageAdmin(admin.ModelAdmin):
    list_display = "id","name"
    list_display_links = "name",
    
class GeneralInformationAdmin(admin.ModelAdmin):
    list_display = "id","name"
    list_display_links = "name",
    
admin.site.register(IndexImage,IndexImageAdmin)
admin.site.register(GeneralInformation,GeneralInformationAdmin)