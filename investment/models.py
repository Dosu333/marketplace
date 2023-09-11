from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from datetime import timedelta
import uuid


TRANSACTION_CHOICES = (
    ('WITHDRAWAL', 'WITHDRAWAL'),
    ('DEPOSIT', 'DEPOSIT'),
)

class AvailableInvestment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=225)
    interest_rate = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    earnings = models.IntegerField()
    image = models.FileField(upload_to='product', null=True, blank=True)
    investment_duration_in_days = models.IntegerField()

    def __str__ (self):
        return self.name
    

class ActiveInvestment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    product = models.ForeignKey(AvailableInvestment, on_delete=models.CASCADE)
    investor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    reference = models.CharField(max_length=225, blank=True, null=True)
    expected_date = models.DateField(blank=True, null=True)
    cashed_out = models.BooleanField(default=False)

    def __str__(self):
        return self.investor.email
    
    def save(self, *args, **kwargs):
        duration = self.product.investment_duration_in_days
        self.expected_date = datetime.now().date() + timedelta(days=duration)
        super(ActiveInvestment, self).save(*args, **kwargs)

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, blank=True, null=True)
    reference = models.CharField(max_length=225, blank=True, null=True)
    amount = models.IntegerField()
    receipient_account_number = models.CharField(max_length=10, blank=True, null=True)
    receipient_bank = models.CharField(max_length=225, blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email