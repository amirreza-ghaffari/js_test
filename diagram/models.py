from django.core.exceptions import ValidationError
from django.db import models
from department.models import Department

from django.utils.translation import gettext_lazy as _

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


class Block(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
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

    class Meta:
        unique_together = ('department', 'label')

    def __str__(self):
        return self.label

    @property
    def loc(self):
        return str(self.loc_height) + ' ' + str(self.loc_length)


class Transition(models.Model):
    label = models.CharField(max_length=256)
    start_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='start_block')
    end_block = models.ForeignKey(Block, on_delete=models.CASCADE,  related_name='end_block')
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('start_block', 'end_block')

    def clean(self):
        if self.start_block == self.end_block:
            raise ValidationError('Start Block and End Block can not be same!')

    @property
    def flow_path(self):
        return str(self.start_block.label) + '_to_' + str(self.end_block.label)

    def __str__(self):
        return self.flow_path


