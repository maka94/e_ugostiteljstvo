from rest_framework import serializers
from apps.residences.models import Residence

class ResidenceSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        residence = super(ResidenceSerializer, self).create(*args, **kwargs)

        residence.owner = self.context['request'].user
        residence.save()

        return residence

    class Meta:
        model = Residence
        fields = ['id','type', 'address', 'town', 'country', 'price', 'bed_number', 'description']

