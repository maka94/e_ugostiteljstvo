from django.shortcuts import render
import os
from rest_framework import viewsets, views, response, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.residences.serializers import ResidenceSerializer
from apps.reservations.models import Reservation
from django.contrib.auth import get_user_model
from apps.residences.models import Residence, ResidenceImage
from datetime import datetime
from django.db.models import Q
from decimal import Decimal
from django.conf import settings
from django.http import FileResponse

User = get_user_model()

class ResidenceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ResidenceSerializer

    def get_queryset(self):
        return Residence.objects.filter(owner=self.request.user, deleted=False)

    def list(self, request, *args, **kwargs):
        response = super(ResidenceViewSet, self).list(request, *args, **kwargs)
        for residence_dict in response.data:
            for image in residence_dict['images']:
                splited = image['image'].split('http://localhost:8000/residences/')
                image['image'] = splited[1]
        return response

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

class AllResidenceView(views.APIView):
    serializer_class = ResidenceSerializer

    def get(self, request):
        queryset = Residence.objects.filter(deleted=False)
        serializer = ResidenceSerializer(queryset, many=True)
        return response.Response(serializer.data)


class SearchResidenceView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    DATE_FORMAT = "%Y-%m-%d"

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

    def _convert_to_decimal(self, param_str, param):
        try:
            return Decimal(param_str)
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
        queryset = Residence.objects.filter(country__iexact=country.lower(), town__iexact=town.lower(), deleted=False)

        # Filter by not required params

        type = request.query_params.get('type')
        if type:
            queryset = queryset.filter(type__iexact=type)

        address = request.query_params.get('address')
        if address:
            queryset = queryset.filter(address__icontains=address)

        price_from_str = request.query_params.get('price_from')
        if price_from_str:
            price_from = self._convert_to_decimal(price_from_str, 'price_from')
            queryset = queryset.filter(price__gte=price_from)


        price_to_str = request.query_params.get('price_to')
        if price_to_str:
            price_to = self._convert_to_decimal(price_to_str, 'price_to')
            queryset = queryset.filter(price__lte=price_to)

        bed_num_str = request.query_params.get('bed_num')
        if bed_num_str:
            bed_num = self._convert_to_int(bed_num_str, 'bed_num')
            queryset = queryset.filter(bed_number=bed_num)

        # filter by dates
        date_to_in_range = Q(date_to__range=[date_from, date_to])
        date_from_in_range = Q(date_from__range=[date_from, date_to])
        dates_in_range = date_to_in_range | date_from_in_range
        surrounding = Q(date_from__lte=date_from, date_to__gte=date_to)

        reservations = Reservation.objects.filter(dates_in_range | surrounding)
        residence_ids = reservations.values_list('residence', flat=True).distinct()
        queryset = queryset.exclude(pk__in=residence_ids)

        # Return what's left
        serializer = ResidenceSerializer(queryset, many=True)
        return response.Response(serializer.data)


class ImageDownloadView(views.APIView):

    def get(self, request, file_name, *args, **kwargs):

        try:
            image = ResidenceImage.objects.get(image=file_name)
        except ResidenceImage.DoesNotExist:
            raise exceptions.NotFound

        return FileResponse(image.image.open())

class ImageUploadView(views.APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        residence_id = request.data['residence_id']
        try:
            residence = Residence.objects.get(id=residence_id, owner=request.user)
        except Residence.DoesNotExist:
            raise exceptions.NotFound

        for image in request.FILES.values():
           ResidenceImage.objects.create(residence=residence, image=image)

        return response.Response()
