from rest_framework import serializers
from apps.residences.models import Residence, Reservation

class ResidenceSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        residence = super(ResidenceSerializer, self).create(*args, **kwargs)

        residence.owner = self.context['request'].user
        residence.save()

        return residence

    class Meta:
        model = Residence
        fields = ['id','type', 'address', 'town', 'country', 'price', 'bed_number', 'description']

class ReservationSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        reservation = super(ReservationSerializer, self).create(*args, **kwargs)
        reservation.user = self.context['request'].user

        reservation.save()

    class Meta:
        model = Reservation
        fields = ['residence', 'date_from', 'date_to']