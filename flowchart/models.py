from django.db import models
from django.urls import reverse


location_choices = (
    ('Danesh', 'Danesh'),
    ('Danesh2', 'Danesh2'),
    ('Gandhi', 'Gandhi'),
    ('Shad Abad', 'Shad Abad'),
    ('Badamak', 'Badamak'),
)


class Flowchart(models.Model):
    name = models.CharField(max_length=256, unique=True)
    location = models.CharField(max_length=256, choices=location_choices, default=None, blank=True, null=True)

    @property
    def get_absolute_url(self):
        return reverse('flowchart:flowchart_view', kwargs={'name': self.name})

    def __str__(self):
        return self.name
