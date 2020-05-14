from rest_framework import serializers
from apps.reservations.models import Reservation
from apps.residences.models import Residence
from apps.residences.serializers import ResidenceSerializer

class CreateReservationSerializer(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()
    residence = serializers.PrimaryKeyRelatedField(queryset=Residence.objects.all())

class ReservationSerializer(serializers.ModelSerializer):
    residence = ResidenceSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'residence', 'date_from', 'date_to', 'cancelled', 'price', 'residence']

