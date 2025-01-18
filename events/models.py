# events/models.py 
from django.db import models
from .choices import event_type_choices
from django.utils import timezone
from PIL import Image

class Event(models.Model):
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50,choices=event_type_choices)
    content = models.TextField(blank=True)
    is_publish = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=timezone.now)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    
    class Meta:
        # Optional: Define ordering of events by publish date (newest first).
        ordering = ['-publish_date']
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return f"{self.title} ({self.event_type}) - {self.publish_date.strftime('%Y-%m-%d')}"

    def save(self):
        super().save()
        img = Image.open(self.photo_main.path)
        if img.height > 500 or img.width >500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.photo_main.path)