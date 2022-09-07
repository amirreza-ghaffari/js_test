from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if value[0:2] != '09' or len(value) != 11:
        raise ValidationError(
            _('not a valid phone number'),
            params={'value': value},
        )

department_choice = (
        ('Legal', 'Legal'),
        ('Risk Audit Compliance', 'RAC'),
        ('Human Recourse', 'HR'),
        ('Marketing', 'Marketing'),
        ('Technology', 'Tech'),
        ('Finance', 'Finance'),
        ('User Experience', 'User Experience'),
        ('Financial', 'Financial'),
        ('Business Development', 'Business Development'),
        ('Operation', 'Operation'),
    )


def get_profile_image_filepath(self, filename):
    return 'profile_images/' + str(self.pk) + '/profile_image.png'


def get_default_profile_image():
    return "default_images/user-profile-default.png"

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(max_length=11, null=True, blank=False, validators=[validate_phone_number])
    first_name = models.CharField(max_length=256, null=True, blank=False)
    last_name = models.CharField(max_length=256, null=True, blank=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    rand_text = models.CharField(max_length=16, default=None, blank=False, null=True)
    department = models.CharField(max_length=256, choices=department_choice, null=True)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True,
                                      default=get_default_profile_image)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email + '-' + self.full_name

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

