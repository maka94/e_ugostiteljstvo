from django.urls import path

from apps.reservations import views

urlpatterns = [
    path('', views.ReservationView.as_view())
]