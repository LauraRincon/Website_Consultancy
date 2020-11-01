from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Project
from .forms import ProjForm

# Create your views here.
def new(request):
    new_form = ProjForm()
    if request.method == 'POST':
        filled_form = ProjForm(request.POST)
        if filled_form.is_valid():
            new_proj = filled_form.save()
            new_pk = new_proj.pk
            note = (
                'Project object with pk \'{}\' was successfully created, \n'
                'Name: {}.'.format(
                    new_pk, filled_form.cleaned_data['name']
                    )
            )
        else:
            note = 'Invalid form values, no project created'
        return render(
            request,
            'new.html',
            {
                'projectform': new_form,
                'note ': note,
                'created_person_pk': new_pk,
            }
        )
    else: 
        note = 'Regiter your new project'
        return render(
            request,
            'new.html',
            {
                'note ': note,
                'projectform' : new_form,
            }
        ) 

def check(request, pk=None):
    if pk:
        try:
            proj = Project.objects.get(pk=pk)
        except:
            raise Http404('Project with pk {} doesn\'t exist',format(pk))
        return render(
            request,
            'check.html',
            {
                'object_pk': proj.pk,
                'object_name': proj.name,
                'object_description': proj.description,
                'object_appointment': proj.appt_date,
            }
        )
    else:
        proj_dict = {}
        for proj in Project.objects.all():
            proj_dict[proj.name] = {
                'pk': proj.pk,
                'description' : proj.description,
                'appt': proj.appt_date,
            }
        return render(
            request,
            'check.html',
            {
                'proj_dict': proj_dict,
            }
        )
