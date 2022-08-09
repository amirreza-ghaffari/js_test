from django.core.exceptions import ValidationError
from django.db import models
from department.models import Department
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from simple_history.models import HistoricalRecords

# Create your models here.

fig_choices = (
        ('Procedure', 'Procedure'),
        ('Cylinder1', 'Cylinder1'),
        ('Terminator', 'Terminator'),
        ('CreateRequest', 'CreateRequest'),
        ('Document', 'Document'),
    )

color_choices = (
    ('pink', 'pink'),
    ('green', 'green'),
    ('black', 'black'),
)


class BlockGroup(models.Model):
    name = models.CharField(max_length=256)
    history = HistoricalRecords()

    def __str__(self):
        return 'Block Group ' + self.name


class Block(models.Model):
    group = models.ForeignKey(BlockGroup, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    label = models.CharField(max_length=256)
    figure = models.CharField(max_length=256, choices=fig_choices, null=True, blank=True)
    description = models.CharField(max_length=256)
    color = models.CharField(max_length=256, choices=color_choices, null=False, default='red')
    thickness = models.IntegerField(default=4,  blank=True, null=True)
    fill = models.CharField(default='lightyellow', max_length=256, blank=True, null=True)
    loc_height = models.IntegerField(null=True, blank=True)
    loc_length = models.IntegerField(null=True, blank=True)
    approved = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('department', 'label')


    @property
    def loc(self):
        return str(self.loc_height) + ' ' + str(self.loc_length)

    @property
    def last_modified(self):
        if self.updated_date:
            return naturaltime(self.updated_date)
        return None

    def __str__(self):
        return self.label


class Transition(models.Model):
    label = models.CharField(max_length=256)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    start_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='start_block')
    end_block = models.ForeignKey(Block, on_delete=models.CASCADE,  related_name='end_block')
    active = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('start_block', 'end_block')

    def clean(self):
        if self.start_block == self.end_block:
            raise ValidationError('Start Block and End Block can not be same!')

    @property
    def flow_path(self):
        return str(self.start_block.label) + '_to_' + str(self.end_block.label)

    @property
    def last_modified(self):
        if self.updated_date:
            return naturaltime(self.updated_date)
        return None

    def __str__(self):
        return self.flow_path


