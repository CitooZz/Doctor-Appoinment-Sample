from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from doctors.filters import DoctorFilters
from doctors.models import Doctor, District, Specialization, Language
from doctors.serializers import (
    DoctorSerializer,
    DistrictSerializer,
    SpecializationSerializer,
    LanguageSerializer,
)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = (
        Doctor.objects.all()
        .select_related("district", "specialization", "language")
        .prefetch_related(
            "opening_hours",
        )
    )
    serializer_class = DoctorSerializer
    filterset_class = DoctorFilters
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = [
        "name",
        "price",
    ]
    search_fields = [
        "name",
        "address",
    ]
    http_method_names = [
        "get",
        "post",
    ]


class SpecializationAPIView(ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class LanguageAPIView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class DistrictAPIView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
