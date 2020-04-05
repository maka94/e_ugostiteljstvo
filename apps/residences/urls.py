from django.urls import path

from apps.residences import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.ResidenceViewSet, basename='residences')
urlpatterns = router.urls