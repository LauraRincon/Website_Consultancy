from django import forms
from .models import Project

class ProjForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            'name',
            'category',
            'description',
            'appt_date',
        ]
        labels = {
            'name': 'Name', 
            'category': 'Category',
            'description': 'Description',
            'appt_date': 'Appointment date',
        }