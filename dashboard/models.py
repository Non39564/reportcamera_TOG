from django.db import models

class DataCamera(models.Model):
    Company = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    date = models.CharField(max_length=255, null=True, blank=True)
    time_in = models.CharField(max_length=255, null=True, blank=True)
    time_out = models.CharField(max_length=255, null=True, blank=True)
    stack = models.IntegerField()
    image_name = models.CharField(max_length=255)
