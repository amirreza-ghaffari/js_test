from django.db import models

# Create your models here.


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


class Department(models.Model):
    name = models.CharField(max_length=256, choices=department_choice, unique=True)

    def __str__(self):
        return self.name



