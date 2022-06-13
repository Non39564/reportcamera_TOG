from django.db import models

class DataCemera(models.Model):
    Company = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    time_in = models.DateTimeField(null=True, blank=True)
    image_name = models.CharField(max_length=255)
