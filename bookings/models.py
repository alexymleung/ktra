from django.db import models
from services.models import Service
from django.contrib.auth.models import User
from django.utils import timezone


class Booking(models.Model):
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Booking Object:S:{self.service}, U:{self.user}, D:{self.order_date}"
