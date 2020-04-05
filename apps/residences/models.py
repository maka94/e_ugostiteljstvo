from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Residence(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    town = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    bed_number = models.IntegerField(default=1)
    deleted = models.BooleanField(default=False)
    description = models.CharField(max_length=255)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    residence = models.ForeignKey(Residence, on_delete=models.DO_NOTHING, null=False)
    date_from = models.DateField()
    date_to = models.DateField()
    cancelled = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)