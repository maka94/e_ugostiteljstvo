from rest_framework import views, response, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.reservations.serializers import CreateReservationSerializer
from apps.reservations.models import Reservation
from django.db.models import Q

class ReservationView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = CreateReservationSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        date_to = input_serializer.validated_data['date_to']
        date_from = input_serializer.validated_data['date_from']
        user = request.user
        residence = input_serializer.validated_data['residence']

        date_to_in_range = Q(date_to__range=[date_from, date_to])
        date_from_in_range = Q(date_from__range=[date_from, date_to])
        dates_in_range = date_to_in_range | date_from_in_range
        surrounding = Q(date_from__lte=date_from, date_to__gte=date_to)

        if residence.reservation_set.filter(dates_in_range | surrounding).exists():
            raise exceptions.ValidationError("Reservation already exists")

        days_td = date_to - date_from
        days = days_td.days
        price_per_night = residence.price
        print(days*price_per_night)
        Reservation.objects.create(
            user=user,
            residence=residence,
            date_from=date_from,
            date_to=date_to,
            price=days*price_per_night
        )
        print(type(date_to))
        print(type(date_from))
        print(input_serializer.validated_data)
        return response.Response("ok")
