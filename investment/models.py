from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
import uuid

class AvailableInvestment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=225)
    interest_rate = models.IntegerField()
    max_earning = models.IntegerField()
    image = models.FileField(upload_to='product', null=True, blank=True)
    investment_duration_in_days = models.IntegerField()

    def __str__ (self):
        return self.name
    

class ActiveInvestment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product = models.ForeignKey(AvailableInvestment, on_delete=models.CASCADE)
    investor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    investment = models.IntegerField()
    reference = models.CharField(max_length=225, blank=True, null=True)
    expected_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.investor.email
    
    def save(self, *args, **kwargs):
        duration = self.product.investment_duration_in_days
        self.expected_date = datetime.now().date() + timedelta(days=duration)
        super(ActiveInvestment, self).save(*args, **kwargs)