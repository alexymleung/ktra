# from django.db import models
# from django.contrib.auth.models import User
# from datetime import datetime

# class Donation(models.Model):
#     donor = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=2)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     address = models.CharField(max_length=200)
#     amount = models.IntegerField()
#     donation_date = models.DateTimeField(default=datetime.now)
#     message = models.TextField(blank=True)
#     payment_type = models.CharField(max_length=200)
#     transaction_date = models.DateTimeField(default=datetime.now)
    
#     def __str__(self):
#         return f"Donation Object: Donor:{self.donor}, Date:{self.donation_date}"