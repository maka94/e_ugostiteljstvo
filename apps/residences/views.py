from django.shortcuts import render
from rest_framework import viewsets, views, response, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.residences.serializers import ResidenceSerializer
from apps.reservations.serializers import ReservationSerializer
from django.contrib.auth import get_user_model
from apps.residences.models import Residence
from datetime import datetime

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



class SearchReservationView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    DATE_FORMAT = "%d-%m-%Y"

    def _format_date(self, date_str, param):
        try:
            return datetime.strptime(date_str, self.DATE_FORMAT).date()
        except ValueError:
            raise exceptions.ValidationError({param: 'Invalid format'})

    def _convert_to_int(self, param_str, param):
        try:
            return int(param_str)
        except ValueError:
            raise exceptions.ValidationError({param: 'Invalid format'})

    def _get_required_param(self, query_params, param):
        try:
            return query_params[param]
        except KeyError:
            raise exceptions.ValidationError({param: 'Missing parameter'})

    def get(self, request):
        # get `date_from` from query params
        date_from_str = self._get_required_param(request.query_params, 'date_from')
        date_from = self._format_date(date_from_str, 'date_from')

        # get `date_to` from query params
        date_to_str = self._get_required_param(request.query_params, 'date_to')
        date_to = self._format_date(date_to_str, 'date_to')

        # get `country` from query params
        country = self._get_required_param(request.query_params, 'country')

        # get `town` from query params
        town = self._get_required_param(request.query_params, 'town')

        # Filter by country & town
        queryset = Residence.objects.filter(country__iexact=country.lower(), town__iexact=town.lower())

        # Filter by not required params

        type = request.query_params.get('type')
        if type:
            queryset = queryset.filter(type__iexact=type)

        address = request.query_params.get('address')
        if address:
            queryset = queryset.filter(address__icontains=address)

        price_from_str = request.query_params.get('price_from')
        if price_from_str:
            price_from = self._convert_to_int(price_from_str, 'price_from')
            queryset = queryset.filter(price__gte=price_from)

        price_to_str = request.query_params.get('price_to')
        if price_to_str:
            price_to = self._convert_to_int(price_to_str, 'price_to')
            queryset = queryset.filter(price__lte=price_to)

        bed_num_str = request.query_params.get('bed_num')
        if bed_num_str:
            bed_num = self._convert_to_int(bed_num_str, 'bed_num')
            queryset = queryset.filter(bed_number=bed_num)

        # filter by dates
        pass

        # Return what's left
        serializer = ResidenceSerializer(queryset, many=True)
        return response.Response(serializer.data)