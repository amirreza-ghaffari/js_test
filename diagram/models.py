from django.core.exceptions import ValidationError
from django.db import models
from department.models import Department
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import Group

# Create your models here.

fig_choices = (
        ('Procedure', 'Procedure'),
        ('Cylinder1', 'Cylinder1'),
        ('Terminator', 'Terminator'),
        ('CreateRequest', 'CreateRequest'),
        ('Document', 'Document'),
        ('Diamond', 'Diamond'),
    )

color_choices = (
    ('pink', 'pink'),
    ('green', 'green'),
    ('black', 'black'),
    ('blue', 'blue'),
    ('red', 'red'),
)


class BlockGroup(models.Model):
    name = models.CharField(max_length=256)
    history = HistoricalRecords()

    def __str__(self):
        return 'Block Group ' + self.name


class Block(models.Model):
    group = models.ForeignKey(BlockGroup, on_delete=models.CASCADE, blank=True, null=True)
    user_groups = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    updated_date = models.DateTimeField(auto_now=True)
    label = models.CharField(max_length=256, null=False, blank=False)
    figure = models.CharField(max_length=256, choices=fig_choices, default='Procedure')
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=256, choices=color_choices, default='black')
    thickness = models.IntegerField(default=4,  blank=True, null=True)
    fill = models.CharField(default='lightyellow', max_length=256)
    loc_height = models.IntegerField(null=True, blank=True)
    loc_length = models.IntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_conditional = models.BooleanField(default=False)
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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_approved:
            self.color = 'green'
        elif self.is_active:
            self.color = 'red'
        elif self.is_conditional:
            self.color = 'blue'
        else:
            self.color = 'black'

        if self.is_conditional:
            self.figure = 'Diamond'
        if self.figure == 'Diamond':
            self.is_conditional = True
        return super(Block, self).save()


class Transition(models.Model):
    label = models.CharField(max_length=256)
    updated_date = models.DateTimeField(auto_now=True)
    start_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='start_block')
    end_block = models.ForeignKey(Block, on_delete=models.CASCADE,  related_name='end_block')
    color = models.CharField(max_length=256, choices=color_choices, default='black')
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('start_block', 'end_block')

    def clean(self):
        if self.start_block == self.end_block:
            raise ValidationError('Start Block and End Block can not be same!')
        if self.is_active is False and self.is_approved:
            raise ValidationError('Can not approve a non active Transition')

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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.is_approved:
            self.color = 'green'
        elif self.is_active:
            self.color = 'red'
        else:
            self.color = 'black'
        return super(Transition, self).save()


