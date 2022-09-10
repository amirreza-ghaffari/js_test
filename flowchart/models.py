from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Location(models.Model):
    name = models.CharField(max_length=256, unique=True)
    incident_number = models.PositiveIntegerField(default=0)

    def increase_incident(self):
        self.incident_number += 1
        self.save()
        return self.incident_number

    def __str__(self):
        return self.name


class Flowchart(models.Model):
    name = models.CharField(max_length=256, unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('name', 'location')

    @property
    def get_absolute_url(self):
        return reverse('flowchart:flowchart_view', kwargs={'name': self.name})

    def clean(self):
        if self.location and self.primary:
            raise ValidationError('Primary Flowchart can not have a location')
        if self.primary and self.is_active:
            raise ValidationError('Primary Flowchart can not activated')

    def __str__(self):
        if self.primary:
            return self.name + ' - primary'
        return self.name + ' - ' + str(self.location)


