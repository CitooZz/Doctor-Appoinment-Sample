from django.db import transaction
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from doctors.models import (
    Doctor,
    OpeningHour,
    Specialization,
    District,
    Language,
)


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = "__all__"
        extra_kwargs = {
            "doctor": {
                "write_only": True,
                "required": False,
                "allow_null": True,
            }
        }

    def validate(self, data):
        weekday = data.get("weekday", "")
        start_hour = data.get("start_hour", "")
        end_hour = data.get("end_hour", "")
        doctor = data.get("doctor")
        is_closed = data.get("is_closed", False)
        if (
            doctor
            and OpeningHour.objects.filter(
                doctor=doctor,
                weekday=weekday,
                start_hour=start_hour,
                end_hour=end_hour,
                is_closed=is_closed,
            ).exists()
        ):
            raise serializers.ValidationError(
                {"opening_hours": [_("Duplicate opening hour.")]}
            )

        if start_hour and end_hour:
            if end_hour <= start_hour:
                raise serializers.ValidationError(
                    _("End hour should be greater than start hour.")
                )

            overlapping_hour = OpeningHour.objects.filter(
                (
                    Q(start_hour__lte=start_hour, end_hour__gte=start_hour)
                    | Q(start_hour__lte=end_hour, end_hour__gte=end_hour)
                )
                & Q(
                    doctor=doctor,
                    weekday=weekday,
                )
            )
            if overlapping_hour.exists():
                raise serializers.ValidationError(
                    {"opening_hours": [_("Opening hour is overlapping.")]}
                )

        return data


class DoctorSerializer(serializers.ModelSerializer):
    opening_hours = OpeningHourSerializer(many=True, allow_empty=False)

    class Meta:
        model = Doctor
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        opening_hours = validated_data.pop("opening_hours")
        doctor = super().create(validated_data)
        for opening_hour in opening_hours:
            opening_hour["doctor"] = doctor.id
            serializer = OpeningHourSerializer(data=opening_hour)
            serializer.is_valid(raise_exception=True)
            serializer.save(doctor=doctor)

        return doctor

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["language"] = LanguageSerializer(instance.language).data
        response["specialization"] = SpecializationSerializer(instance.language).data
        response["district"] = DistrictSerializer(instance.district).data
        return response
