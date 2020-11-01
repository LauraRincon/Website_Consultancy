from django.db import models

# Create your models here.

CATEGORY = [
    ('Fotovoltic','Fotovoltic'),
    ('Design','Design')
]

class Project(models.Model):
    name = models.CharField(max_length=20)
    category = models.CharField(max_length=20,choices=CATEGORY)
    description = models.CharField(max_length=200)
    appt_date = models.DateTimeField('appointment date')
