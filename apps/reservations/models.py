from django.db import models
from django.contrib.auth import get_user_model
from apps.residences.models import Residence

User =  get_user_model()

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    residence = models.ForeignKey(Residence, on_delete=models.DO_NOTHING, null=False)
    date_from = models.DateField()
    date_to = models.DateField()
    cancelled = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
