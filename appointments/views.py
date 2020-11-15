from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.safestring import mark_safe

from .models import Client, Project
from .forms import ProjForm, ClientForm
from .utils import Calendar

# Create your views here.
def index(request):
    return render(
        request,
        'index.html',
    )

def singup(request):
    new_form = ClientForm()
    if request.method == 'POST':
        filled_form = ClientForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            note = "Your registry was succesful! Please go back to the \
                    homepage and log in"
            staff = request.POST.get("staff")
            if staff:
                new_user = Client.objects.get(
                    username=request.POST.get('username'))
                print(new_user)
                print(new_user.is_staff)
                new_user.is_staff = True
                new_user.save()
                print(new_user.is_staff)
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
        note = ' '
        return render(
            request,
            'singup.html',
            {
                'note': note,
                'clientform': new_form,
            }
        )

@login_required
def new(request):
    new_form = ProjForm()
    cal = calendar(request)
    choices = []
    for user in Client.objects.filter(is_staff=False):
        choices.append(user)

    if request.method == 'POST':

        filled_form = ProjForm(request.POST)
        if filled_form.is_valid():
            if request.user.is_staff:
                user = Client.objects.get(
                    id=request.POST.get('username_choice'))
            else:
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
                'calendar': cal,
                'choices': choices,
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
                'calendar': cal,
                'choices': choices,
            }
        )

@login_required
def calendar(request):
    date = datetime.today()
    cal = Calendar(date.year, date.month)
    html_cal = cal.formatmonth(withyear=True)
    context = mark_safe(html_cal)
    return context

@login_required
def check(request, pk=None, id=None):
    if request.user.is_staff and pk is None:
        proj_dict = {}
        for proj in Project.objects.all():
            dict_name = proj.name + ": " + str(proj.client)
            proj_dict[dict_name] = {
                'pk': proj.pk,
                'place': proj.place,
                'billing': proj.billing,
                'category': proj.category,
                'appt': proj.appt_date,
                'uid': proj.client.pk,
                'client': proj.client,
            }
        return render(
            request,
            'check.html',
            {
                'proj_dict': proj_dict,
            }
        )
    else:
        if id == request.user.id or request.user.is_staff:
            client = Client.objects.get(pk=id)

            if pk:
                try:
                    proj = Project.objects.get(client=client, pk=pk)
                except Project.DoesNotExist:
                    raise Http404(
                        'Project with pk {} doesn\'t exist'.format(pk))
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
                        'object_client': proj.client,
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

@login_required
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

@login_required
def modify(request, pk=None):
    note = ''
    cal = calendar(request)
    if request.method == 'POST':
        filled_form = ProjForm(request.POST)
        try:
            if request.user.is_staff:
                old_proj = Project.objects.get(pk=pk)
            else:
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
                'calendar': cal,
                'projectform': new_form,
                'note': note,
                'project_pk': pk,
            }
        )
    else:
        note = ''
        try:
            if request.user.is_staff:
                old_proj = Project.objects.get(pk=pk)
            else:
                old_proj = Project.objects.get(client=request.user.id, pk=pk)
        except Project.DoesNotExist:
            raise Http404('Project with pk {} doesn\'t exist'.format(pk))
        old_form = ProjForm(instance=old_proj)
        return render(
            request,
            'modify.html',
            {
                'calendar': cal,
                'note': note,
                'projectform': old_form,
                'project_pk': pk,
            }
        )
