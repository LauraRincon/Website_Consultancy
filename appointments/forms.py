from django import forms
from .models import Project


class ProjForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ["client"]
        fields = [
            'name',
            'place',
            'billing',
            'category',
            'appt_date',
        ]
        labels = {
            'name': 'Name',
            'place': 'Place',
            'billing': 'Billing',
            'category': 'Category',
            'appt_date': 'Appointment date',
        }
