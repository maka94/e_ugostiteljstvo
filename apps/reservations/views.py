from rest_framework import  viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.reservations.serializers import ReservationSerializer

class ReservationView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return ReservationView.objects.filter(user=self.request.user, cancelled=False)

    def perform_destroy(self, instance):
        instance.cancelled = True
        instance.save()
