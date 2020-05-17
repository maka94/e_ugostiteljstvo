from django.urls import path

from apps.residences import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.ResidenceViewSet, basename='residences')


urlpatterns = router.urls + [
    path('search', views.SearchResidenceView.as_view()),
    path('all', views.AllResidenceView.as_view()),
    path('download/<str:file_name>', views.ImageDownloadView.as_view()),
]
