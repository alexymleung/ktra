from django.contrib import admin
from .models import IndexImage

class IndexImageAdmin(admin.ModelAdmin):
    list_display = "id","name"
    list_display_links = "name",
    
admin.site.register(IndexImage,IndexImageAdmin)
