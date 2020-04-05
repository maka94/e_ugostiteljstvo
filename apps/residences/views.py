from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.residences.serializers import ResidenceSerializer, ReservationSerializer
from django.contrib.auth import get_user_model
from apps.residences.models import Residence

User = get_user_model()

class ResidenceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResidenceSerializer

    def get_queryset(self):
        return Residence.objects.filter(owner=self.request.user, deleted=False)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

class ReservationView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return ReservationView.objects.filter(user=self.request.user, cancelled=False)

    def perform_destroy(self, instance):
        instance.cancelled = True
        instance.save()


