from django.db import models
from django.urls import reverse

class Flowchart(models.Model):
    name = models.CharField(max_length=256, unique=True)

    @property
    def get_absolute_url(self):
        return reverse('flowchart:flowchart_view', kwargs={'name': self.name})

    def __str__(self):
        return self.name
