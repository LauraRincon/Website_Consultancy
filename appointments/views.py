from urllib.parse import urlencode
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.safestring import mark_safe

from .models import Client, Project
from .forms import ProjForm
from .utils import Calendar


# Create your views here.
@login_required
def new(request):
    new_form = ProjForm()
    if request.method == 'POST':
        filled_form = ProjForm(request.POST)
        if filled_form.is_valid():
            user = Client.objects.get(id=request.user.id)
            new_proj = filled_form.save(commit=False)
            new_proj.client = user
            new_proj.save()
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

# @login_required
# def get_date(req_day):
#     if req_day:
#         year,month = (int(x) for x in req_day.split('-'))
#         return date(year, month, day=1)
#     return datetime.today()

@login_required
def calendar(request, id):
    date = datetime.today()
    cal = Calendar(id, date.year, date.month)
    html_cal = cal.formatmonth(id, withyear=True)
    context = mark_safe(html_cal)
    # context['prev_month'] = prev_month(d)
    # context['next_month'] = next_month(d)
    return context

@login_required
def check(request, pk=None, id=None):
    if id==request.user.id:
        try:
            client = Client.objects.get(pk=id)
            cal= calendar(request,id)
            if pk:
                try:
                    proj = Project.objects.get(client=client, pk=pk)
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
                except Project.DoesNotExist:
                    raise Http404('Project with pk {} doesn\'t exist'.format(pk))
            else:
                proj_dict = {}
                for proj in client.project_set.all():
                    proj_dict[proj.name] = {
                        'pk': proj.pk,
                        'place': proj.place,
                        'billing': proj.billing,
                        'category': proj.category,
                        'appt': proj.appt_date,
                        'uid' : id
                    }
                return render(
                request,
                'check.html',
                {
                    'proj_dict': proj_dict,
                    'calendar': cal,
                }
                )
        except Client.DoesNotExist:
            raise Http404('User with id {} doesn\'t exist'.format(id))
    else:
        client = Client.objects.get(pk=request.user.id)
        base_url = '/check/'
        query_string =  urlencode({'id': (client.pk)})
        url = '{}{}'.format(base_url, query_string)  
        return HttpResponseRedirect(url)