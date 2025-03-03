from django.db import models
from django.utils import timezone

class ClimateData(models.Model):
    temperature = models.FloatField(verbose_name="Temperature")
    humidity = models.FloatField(verbose_name="Humidity")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date")

    def __str__(self):
        return f"{self.timestamp}: {self.temperature}°C, {self.humidity}%"

