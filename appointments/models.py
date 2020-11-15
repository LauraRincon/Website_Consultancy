from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

import datetime

# Create your models here.

CATEGORY = [
    ('Residential', 'Residential'),
    ('Comercial', 'Comercial'),
    ('Industrial', 'Industrial'),
    ('Medium Voltage Industrial', 'Medium Voltage Industrial'),
    ('Large Scale', 'Large Scale')
]


class Client(AbstractUser):
    tel = models.CharField(max_length=20, default='')
    enterprise = models.CharField(max_length=20, default='')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Project(models.Model):
    name = models.CharField(max_length=20, default='')
    place = models.CharField(max_length=30, default='')
    billing = models.CharField(max_length=15, default='')
    category = models.CharField(max_length=50, choices=CATEGORY)
    appt_date = models.DateTimeField('appointment date')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "{} - <<{}>>".format(self.name, self.appt_date)
