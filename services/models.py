from django.db import models
from django.utils import timezone
from .choices import service_type_choices
from PIL import Image

class Service(models.Model):
    title = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50,choices=service_type_choices.items())
    description = models.TextField(blank=True)
    service_date = models.DateField(default=timezone.now)
    service_start_time = models.DateTimeField(default=timezone.now)
    service_end_time = models.DateTimeField(default=timezone.now)
    fee = models.IntegerField(default=0)
    quota = models.IntegerField(blank=True)
    is_publish = models.BooleanField(default=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d',blank=True)
        
    def __str__(self):
        return f"Service Object:Title{self.title}"

    def save(self):
        super().save()
        img = Image.open(self.photo_main.path)
        if img.height > 500 or img.width >500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.photo_main.path)