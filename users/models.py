from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.exceptions import ValidationError
from flowchart.models import Flowchart


def validate_phone_number(value):
    if value[0:2] != '09' or len(value) != 11:
        raise ValidationError(
            _('not a valid phone number'),
            params={'value': value},
        )


def validate_email(value):
    if value.split('@')[-1] != 'digikala.com':
        raise ValidationError(
            _('Email must be in Digikala domain'),
            params={'value': value},
        )


department_choice = (
        ('Legal', 'Legal'),
        ('Risk Audit Compliance', 'RAC'),
        ('Human Recourse', 'HR'),
        ('Marketing', 'Marketing'),
        ('Technology', 'Tech'),
        ('Finance', 'Finance'),
        ('Customer Experience', 'Customer Experience'),
        ('Financial', 'Financial'),
        ('Business Development', 'Business Development'),
        ('commercial', 'commercial'),
        ('security', 'security'),
        ('HSE', 'HSE'),
        ('Customer Service', 'CS'),
        ('Operation', 'Operation'),
        ('Product', 'Product'),
        ('Logistic, Express', 'Logistic, Express'),
    )


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return "default_images/user-profile-default.png"


def get_member_profile_image_filepath(self, filename):
    return 'member_profile_images'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=256, null=True, blank=False)
    last_name = models.CharField(max_length=256, null=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    rand_text = models.CharField(max_length=16, default=None, blank=False, null=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)
    mobile_number = models.CharField(max_length=11, null=True, blank=False, validators=[validate_phone_number],
                                     unique=True)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        full_name = ''
        if self.last_name:
            full_name = self.last_name
        if self.first_name:
            full_name = self.first_name + ' ' + full_name
        return full_name

    class Meta:
        # Add verbose name
        verbose_name = 'User'


class Member(models.Model):
    email = models.EmailField(_('email address'), unique=True,  validators=[validate_email])
    mobile_number = models.CharField(max_length=11, null=True, blank=False, validators=[validate_phone_number], unique=True)
    first_name = models.CharField(max_length=256, null=True, blank=False)
    last_name = models.CharField(max_length=256, null=True, blank=False)
    department = models.CharField(max_length=256, choices=department_choice, null=False, blank=False)
    profile_image = models.ImageField(upload_to='member_profile_images/', null=True, blank=True,
                                      default=get_default_profile_image)

    def __str__(self):
        return self.last_name + ' - ' + self.first_name

    @property
    def full_name(self):
        return self.last_name + ' - ' + self.first_name


class EmailResponse(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='email_res')
    message = models.TextField()
    flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE, related_name='email_res', null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.member.email

    class Meta:
        unique_together = ('member', 'message')
