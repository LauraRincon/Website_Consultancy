from urllib.parse import urlencode
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Client, Project
from .forms import ProjForm, ClientForm


# Create your views here.
@login_required
def new(request):
    new_form = ProjForm()
    if request.method == 'POST':
        filled_form = ProjForm(request.POST)
        if filled_form.is_valid():
            user = Client.objects.get(id=request.user.id)
            new_proj = filled_form.save(commit=False)

            dateAvailable = True
            for project in Project.objects.all():
                if project.appt_date == new_proj.appt_date:
                    dateAvailable = False
                    break

            if dateAvailable:
                new_proj.client = user
                new_proj.save()
                new_pk = new_proj.pk
                note = (
                    'Project object with pk \'{}\' was successfully created,\n'
                    'Name: {}.'.format(
                        new_pk, filled_form.cleaned_data['name']
                        )
                )
            else:
                note = 'That date is not available.'
        else:
            note = 'Invalid form values, no project created'
        return render(
            request,
            'new.html',
            {
                'projectform': new_form,
                'note': note,
            }
        )
    else:
        note = 'Regiter your new project'
        return render(
            request,
            'new.html',
            {
                'note': note,
                'projectform': new_form,
            }
        )


@login_required
def check(request, pk=None, id=None):
    if id == request.user.id:
        try:
            client = Client.objects.get(pk=id)
        except Client.DoesNotExist:
            raise Http404('User with id {} doesn\'t exist'.format(id))
        if pk:
            try:
                proj = Project.objects.get(client=client, pk=pk)
            except Project.DoesNotExist:
                raise Http404('Project with pk {} doesn\'t exist'.format(pk))
            return render(
                request,
                'check.html',
                {
                    'object_pk': proj.pk,
                    'object_name': proj.name,
                    'object_place': proj.place,
                    'object_billing': proj.billing,
                    'object_category': proj.category,
                    'object_appointment': proj.appt_date,
                }
            )
        else:
            proj_dict = {}
            for proj in client.project_set.all():
                proj_dict[proj.name] = {
                    'pk': proj.pk,
                    'place': proj.place,
                    'billing': proj.billing,
                    'category': proj.category,
                    'appt': proj.appt_date,
                    'uid': id
                }
            return render(
                request,
                'check.html',
                {
                    'proj_dict': proj_dict,
                }
            )
    else:
        client = Client.objects.get(pk=request.user.id)
        base_url = '/check/'
        query_string = urlencode({'id': (client.pk)})
        url = '{}{}'.format(base_url, query_string)
        return HttpResponseRedirect(url)


def delete(request, pk=None):
    if pk is not None and request.method == 'POST':
        proj = Project.objects.get(pk=pk)
        proj.delete()
        return redirect('/check')
    else:
        return render(
            request,
            'delete.html'
        )


def singup(request):
    new_form = ClientForm()
    if request.method == 'POST':
        filled_form = ClientForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            note = "Your registry was succesful! Please go back to the \
                    homepage and log in"
        else:
            note = 'Invalid form values, no user created'
        return render(
            request,
            'singup.html',
            {
                'clientform': new_form,
                'note': note,
                'formErrors': filled_form.errors.as_data()
            }
        )
    else:
        note = 'Regiter your user'
        return render(
            request,
            'singup.html',
            {
                'note': note,
                'clientform': new_form,
            }
        )


@login_required
def modify(request, pk=None):
    note = ''
    if request.method == 'POST':
        filled_form = ProjForm(request.POST)
        try:
            old_proj = Project.objects.get(client=request.user.id, pk=pk)
        except Project.DoesNotExist:
            raise Http404('Project with pk {} doesn\'t exist'.format(pk))
        if filled_form.is_valid():
            user = Client.objects.get(id=request.user.id)
            new_proj = filled_form.save(commit=False)
            old_proj.delete()

            dateAvailable = True
            for project in Project.objects.all():
                if project.appt_date == new_proj.appt_date:
                    dateAvailable = False
                    break

            if dateAvailable:
                new_proj.client = user
                new_proj.save()
                new_pk = new_proj.pk
                note = (
                    'Project object with pk \'{}\' was successfully modified, '
                    'Name: {}.'.format(
                     new_pk, filled_form.cleaned_data['name'])
                )
                new_form = filled_form
                pk = new_pk
            else:
                note = 'That date is not available.'
                new_form = ProjForm(instance=old_proj)
        else:
            note = 'Invalid form values, project not modified'
            new_form = ProjForm(instance=old_proj)
        return render(
            request,
            'modify.html',
            {
                'projectform': new_form,
                'note': note,
                'project_pk': pk
            }
        )
    else:
        note = 'Modify project'
        try:
            old_proj = Project.objects.get(client=request.user.id, pk=pk)
        except Project.DoesNotExist:
            raise Http404('Project with pk {} doesn\'t exist'.format(pk))
        old_form = ProjForm(instance=old_proj)
        return render(
            request,
            'modify.html',
            {
                'note': note,
                'projectform': old_form,
                'project_pk': pk,
            }
        )


def index(request):
    return render(
        request,
        'index.html',
    )
