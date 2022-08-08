from django_filters import rest_framework as filters

from doctors.models import Doctor


class DoctorFilters(filters.FilterSet):
    start_price = filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )
    end_price = filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    class Meta:
        model = Doctor
        fields = (
            "district",
            "specialization",
            "language",
        )
