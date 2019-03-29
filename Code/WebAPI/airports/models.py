from django.db import models
from django import forms
import datetime


# Create your models here.


class UpdateForm(forms.Form):
    cancelled = forms.CharField(label="Cancelled", max_length=50)
    on_time = forms.CharField(label="First On Time", max_length=50)
    diverted = forms.CharField(label="Diverted", max_length=50)
    delayed = forms.CharField(label="Delated", max_length=50)


    class Meta:
        verbose_name_plural = "UpdateForm"


class Airports(models.Model):
    code = models.CharField(null=False, max_length=3)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "Airports"


class AirportCarriers(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "AirportCarriers"


class Flights(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)
    date = models.DateField(null=False, default=datetime.datetime.now)
    cancelled = models.IntegerField()
    on_time = models.IntegerField()
    total = models.IntegerField()
    delayed = models.IntegerField()
    diverted = models.IntegerField()

    class Meta:  # to make the plural less awkward
        verbose_name_plural = "Flights"


class Delays(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)
    date = models.DateField(null=False, default=datetime.datetime.now)
    late_aircraft = models.IntegerField()
    weather = models.IntegerField()
    security = models.IntegerField()
    nas = models.IntegerField()
    carrier_delay = models.IntegerField()

    class Meta:  # to make the plural less awkward
        verbose_name_plural = "Delays"


class MinutesDelayed(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)
    date = models.DateField(null=False, default=datetime.datetime.now)
    late_aircraft = models.IntegerField()
    weather = models.IntegerField()
    carrier_delay = models.IntegerField()
    security = models.IntegerField()
    total = models.IntegerField()
    nas = models.IntegerField()

    def __str__(self):  # this is just for the admin page
        return self.total

    class Meta:  # to make the plural less awkward
        verbose_name_plural = "MinutesDelayed"
