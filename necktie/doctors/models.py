from decimal import Decimal

from django.db.models import Q
from django.core.validators import MinValueValidator
from django.db import models


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.ForeignKey(Specialization, on_delete=models.PROTECT)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    is_price_inclusive = models.BooleanField(default=False)

    address = models.TextField()
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    language = models.ForeignKey(Language, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class WeekdayChoices(models.TextChoices):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    PUBLIC_HOLIDAY = "Public Holiday"


class OpeningHour(models.Model):
    doctor = models.ForeignKey(
        Doctor, related_name="opening_hours", on_delete=models.CASCADE
    )

    weekday = models.CharField(max_length=14, choices=WeekdayChoices.choices)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "doctor",
                    "weekday",
                    "start_hour",
                    "end_hour",
                ],
                condition=Q(start_hour__isnull=False) & Q(end_hour__isnull=False),
                name="unique_doctor_opening_hour",
            ),
            models.UniqueConstraint(
                fields=[
                    "doctor",
                    "weekday",
                    "is_closed",
                ],
                condition=Q(is_closed=True),
                name="unique_doctor_closed_hour",
            ),
        ]

    def __str__(self):
        return self.weekday
