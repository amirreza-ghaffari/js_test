from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from jsonfield import JSONField
from django_jalali.db import models as jmodels
from .storage import OverwriteStorage
import jdatetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


def screenshot_path(self, filename):
    return 'screenshots/' + str(self.flowchart.id) + '/' + filename


def severity_path(self, filename):
    return 'severity/' + str(self.flowchart.id) + '/' + filename


class Location(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Flowchart(models.Model):
    name = models.CharField(max_length=256)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    triggered_date = models.DateTimeField(null=True, blank=True)
    incident_counter = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('name', 'location')

    @property
    def get_absolute_url(self):
        return reverse('flowchart:flowchart_view', kwargs={'pk': self.id})

    def increase_incident(self):
        self.incident_counter += 1
        self.save()
        return self.incident_counter

    def clean(self):
        if self.location and self.primary:
            raise ValidationError('Primary Flowchart can not have a location')
        if self.primary and self.is_active:
            raise ValidationError('Primary Flowchart can not activated')

    def __str__(self):
        if self.primary:
            return self.name.replace('_', ' ') + ' - primary'

        if self.location.name.lower() == 'no location':
            return self.name.replace('_', ' ') + ' (No location provided)'
        return self.name.replace('_', ' ') + ' - ' + str(self.location)

    def p_triggered_date(self):
        if self.triggered_date:
            t = self.triggered_date
            return str(jdatetime.datetime.fromgregorian(day=t.day, month=t.month, year=t.year,
                                                    hour=t.hour, minute=t.minute))
        return None


class HistoryChange(models.Model):
        flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE)
        comment_history = JSONField(default=dict)
        block_history = JSONField(default=dict)
        email_response = JSONField(default=dict)
        initial_date = models.DateTimeField()
        j_initial_date = jmodels.jDateField(null=True, blank=True)

        def __str__(self):
            return self.flowchart.name + str(self.initial_date)

        def convert_to_j(self):
            j = jdatetime.datetime.fromgregorian(day=self.initial_date.day, month=self.initial_date.month,
                                             year=self.initial_date.year, hour=self.initial_date.hour,
                                             minute=self.initial_date.minute)
            return j

        def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
            self.j_initial_date = self.convert_to_j()
            return super(HistoryChange, self).save()


class ContingencyPlan(models.Model):
    developed = models.PositiveIntegerField(default=0)
    in_progress = models.PositiveIntegerField(default=0)
    not_developed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'Contingency plans progress'


class Screenshot(models.Model):
    flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE, related_query_name='screenshot')
    image = models.ImageField(upload_to=screenshot_path, storage=OverwriteStorage)

    def __str__(self):
        return self.flowchart.name

    def save(self, *args, **kwargs):
        try:
            img = Screenshot.objects.get(flowchart__name=self.flowchart.name)
            img.delete()
        except Screenshot.DoesNotExist:
            pass

        img = Image.open(self.image)
        width, height = img.size
        margin = 0
        box = (int(width*margin), int(height*margin), int(width*(1-margin)), int(height*(1-margin)))
        img = img.crop(box)

        buffer = BytesIO()
        img.save(fp=buffer, format='png')
        content = ContentFile(buffer.getvalue())
        cropped_image = InMemoryUploadedFile(
            content,  # file
            None,  # field_name
            self.image.name,  # file name
            'image/png',  # content_type
            content.tell,  # size
            None)  # content_type_extra

        self.image = cropped_image
        super(Screenshot, self).save(*args, **kwargs)


class CrisisSeverityImage(models.Model):
    image = models.ImageField(upload_to=severity_path, storage=OverwriteStorage)
    flowchart = models.OneToOneField(Flowchart, on_delete=models.CASCADE, related_query_name='severity_image')

    class Meta:
        verbose_name = 'Crisis Image'
        verbose_name_plural = 'Crisis Images'

    def __str__(self):
        return self.flowchart.name.replace('_', ' ').title()

    def save(self, *args, **kwargs):

        self.image.name = str(self.flowchart.id) + '.png'
        super(CrisisSeverityImage, self).save(*args, **kwargs)

