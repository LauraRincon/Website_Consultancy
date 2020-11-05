from django.db import models

# Create your models here.

CATEGORY = [
    ('Residential', 'Residential'),
    ('Comertial', 'Comertial'),
    ('Industrial', 'Industrial'),
    ('Medium Voltage Industrial', 'Medium Voltage Industrial'),
    ('Large Scale', 'Large Scale')
]

class User(models.Model):
    first_name = models.CharField(max_length=20, default='userUnknown')
    last_name = models.CharField(max_length=20, default='')
    email = models.EmailField(max_length=254)
    tel = models.CharField(max_length=20, default='')
    enterprise = models.CharField(max_length=20, default='')
    password =  models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.first_name)

class Project(models.Model):
    name = models.CharField(max_length=20, default='')
    place = models.CharField(max_length=30, default='')
    billing = models.CharField(max_length=15, default='')
    category = models.CharField(max_length=50, choices=CATEGORY)
    # user
    appt_date = models.DateTimeField('appointment date')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 

    def __str__(self):
        return "{} - <<{}>>".format(self.name, self.appt_date)

