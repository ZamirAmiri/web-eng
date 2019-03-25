from django.db import models
import datetime

# Create your models here.

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
    date    = models.DateField(null=False, default=datetime.datetime.now)
    cancelled = models.IntegerField()
    on_time = models.IntegerField()
    total = models.IntegerField()
    delayed = models.IntegerField()
    diverted = models.IntegerField()

    def __str__(self): #this is just for the admin page
        return self.code

    class Meta: #to make the plural less awkward
        verbose_name_plural = "Flights"

class Delays(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)
    date    = models.DateField(null=False, default=datetime.datetime.now)
    late_aircraft = models.IntegerField()
    weather = models.IntegerField()
    security = models.IntegerField()
    nas = models.IntegerField()
    carrier_delay = models.IntegerField()

    def __str__(self):  # this is just for the admin page
        return self.code

    class Meta:  # to make the plural less awkward
        verbose_name_plural = "Delays"

class MinutesDelayed(models.Model):
    airport = models.CharField(null=False, max_length=3)
    carrier = models.CharField(null=False, max_length=3)
    date    = models.DateField(null=False, default=datetime.datetime.now)
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