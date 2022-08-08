from django.urls import path, include
from rest_framework.routers import DefaultRouter

from doctors.views import (
    DoctorViewSet,
    DistrictAPIView,
    SpecializationAPIView,
    LanguageAPIView,
)


router = DefaultRouter()
router.register("doctors", DoctorViewSet, basename="doctors")

urlpatterns = [
    path("", include(router.urls)),
    path("districts/", DistrictAPIView.as_view()),
    path("specializations/", SpecializationAPIView.as_view()),
    path("languages/", LanguageAPIView.as_view()),
]
