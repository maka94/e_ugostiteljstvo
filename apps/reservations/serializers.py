from rest_framework import serializers
from apps.reservations.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        reservation = super(ReservationSerializer, self).create(*args, **kwargs)
        reservation.user = self.context['request'].user

        reservation.save()

    class Meta:
        model = Reservation
        fields = ['residence', 'date_from', 'date_to']