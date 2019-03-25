from django.db import models

# Create your models here.

class Carriers(models.Model):
    code = models.CharField(null=False, max_length=3)
    name = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = "Carriers"