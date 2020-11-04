from django.db import models

# Create your models here.

CATEGORY = [
    ('Residential', 'Residential'),
    ('Comertial', 'Comertial'),
    ('Industrial', 'Industrial'),
    ('Medium Voltage Industrial', 'Medium Voltage Industrial'),
    ('Large Scale', 'Large Scale')
]


class Project(models.Model):
    name = models.CharField(max_length=20, default='')
    place = models.CharField(max_length=30, default='')
    billing = models.CharField(max_length=15, default='')
    category = models.CharField(max_length=50, choices=CATEGORY)
    # user
    appt_date = models.DateTimeField('appointment date')
