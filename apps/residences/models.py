from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Residence(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    coords = models.IntegerField(default=1)
    town = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    bed_number = models.IntegerField(default=1)
    deleted = models.BooleanField(default=False)
    description = models.CharField(max_length=255)

class ResidenceImage(models.Model):
    residence = models.ForeignKey(Residence, on_delete=models.DO_NOTHING, null=False, related_name='images')
    image = models.FileField()

