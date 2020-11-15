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

class StaffProjForm(ProjForm):
    choices = ()
    for user in Client.objects.filter(is_staff=False):
        choices += ((user.id, user.username),)
    client = forms.ChoiceField(choices=choices)


    class Meta(ProjForm.Meta):
        fields = ProjForm.Meta.fields + ['client',]

class ClientForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Client
        exclude = []
        fields = UserCreationForm.Meta.fields + (
                'email',
                'first_name',
                'last_name',
                'tel',
                'enterprise')
        labels = {
            'tel': 'Phone Number',
            'enterprise': 'Enterprise',
        }
