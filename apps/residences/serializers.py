from rest_framework import serializers
from apps.residences.models import Residence, ResidenceImage
from django.contrib.auth import get_user_model

User = get_user_model()

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ResidenceImageSerializer(serializers.Serializer):
    image = serializers.FileField()

class ResidenceSerializer(serializers.ModelSerializer):

    def create(self, *args, **kwargs):
        residence = super(ResidenceSerializer, self).create(*args, **kwargs)

        residence.owner = self.context['request'].user
        residence.save()

        return residence
    owner = OwnerSerializer(read_only=True)
    images = ResidenceImageSerializer(many=True)
    class Meta:
        model = Residence
        fields = ['id','type', 'address', 'town', 'country', 'price', 'bed_number', 'description', 'owner', 'images']

