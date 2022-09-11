from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.humanize.templatetags.humanize import naturaltime
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import Group
from flowchart.models import Flowchart
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

fig_choices = (
        ('Procedure', 'Procedure'),
        ('Cylinder1', 'Cylinder1'),
        ('Terminator', 'Terminator'),
        ('CreateRequest', 'CreateRequest'),
        ('Document', 'Document'),
        ('Diamond', 'Diamond')
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

    def __str__(self):
        return 'Block Group ' + self.name


class Block(models.Model):
    group = models.ForeignKey(BlockGroup, on_delete=models.CASCADE, blank=True, null=True)
    user_groups = models.ManyToManyField(Group, blank=True, null=True)
    flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE, related_name='flowchart')
    updated_date = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=256, null=False, blank=False)
    figure = models.CharField(max_length=256, choices=fig_choices, default=None, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=256, choices=color_choices, default='black')
    loc_height = models.IntegerField(null=True, blank=True)
    loc_length = models.IntegerField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_conditional = models.BooleanField(default=False)
    rand_text = models.CharField(max_length=16, default=None, blank=False, null=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('flowchart', 'label')

    @property
    def loc(self):
        return str(self.loc_height) + ' ' + str(self.loc_length)

    @property
    def last_modified(self):
        if self.updated_date:
            return naturaltime(self.updated_date)
        return None

    def __str__(self):
        return self.label + " (" + str(self.flowchart) + ")"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_approved:
            self.color = 'green'
        elif self.is_active:
            self.color = 'red'
        else:
            self.color = 'black'

        if self.is_conditional:
            self.figure = 'Diamond'
        if self.figure == 'Diamond':
            self.is_conditional = True
        return super(Block, self).save()


class Transition(models.Model):
    flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE, related_name='transition_flowchart')
    label = models.CharField(max_length=256)
    updated_date = models.DateTimeField(auto_now=True)
    start_block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='out_transition')
    end_block = models.ForeignKey(Block, on_delete=models.CASCADE,  related_name='input_transition')
    color = models.CharField(max_length=256, choices=color_choices, default='black')
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    history = HistoricalRecords()

    class Meta:
        unique_together = ('start_block', 'end_block', 'flowchart')

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


class Comment(models.Model):
    label = models.CharField(max_length=256, null=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='block')
    updated_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return (self.label or '') + self.author.full_name

    @property
    def last_modified(self):
        if self.updated_date:
            return naturaltime(self.updated_date)
        return None



