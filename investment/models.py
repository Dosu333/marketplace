from django.db import models
from django.contrib.auth import get_user_model
import uuid

class AvailableInvestment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=225)
    interest_rate = models.IntegerField()
    investment = models.IntegerField()
    max_earning = models.IntegerField()
    image = models.FileField(upload_to='product', null=True, blank=True)
    investment_duration = models.IntegerField()
    investors = models.ManyToManyField(get_user_model())

    def __str__ (self):
        return self.name