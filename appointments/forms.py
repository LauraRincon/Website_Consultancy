from django import forms
from .models import Project, Client
from django.contrib.auth.forms import UserCreationForm


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


class ClientForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Client
        exclude = []
        fields = UserCreationForm.Meta.fields + ('tel', 'enterprise')
        labels = {
            'tel': 'Phone Number',
            'enterprise': 'Enterprise',
        }
