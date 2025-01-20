from django.db import models

class IndexImage(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='photos/%Y/%m/%d')
    is_shown = models.BooleanField(default=True)
    
class GeneralInformation(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=100)