from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import User, Project
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
                'note': note,
                # 'created_person_pk': new_pk,
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


def check(request, pk=None, id=None):
    if id:
        try:
            user = User.objects.get(pk=id)
            if pk:
                try:
                    proj = Project.objects.get(user=user, pk=pk)
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
                for proj in user.project_set.all():
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
                }
                )
        except User.DoesNotExist:
            raise Http404('User with id {} doesn\'t exist'.format(id))
    else:
        return render(
            request,
            'check.html'
        )