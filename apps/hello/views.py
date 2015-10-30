import json
from time import strftime

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import About, AllRequest
from .forms import EditPersonForm


def all_people(request):
    people = About.objects.order_by('id')[:1]
    return render(request, 'hello/about.html', {'people': people})


def request_list(request):
    requests = AllRequest.objects.order_by('-id')[:10]
    return render(request, 'hello/request.html', {'requests': requests})


@csrf_exempt
def ajax_request_list(request):
    requests = AllRequest.objects.order_by('-id')[:10]
    data = [{'req_id': req.id, 
             'req_date': req.date.strftime("%d/%b/%Y %H:%M:%S"), 
             'req_method': req.method,
             'req_path': req.path} for req in requests]
    data.reverse()
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def edit_person(request, pk):
    person = get_object_or_404(About, pk=pk)
    if request.method == "POST":
        form = EditPersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            if request.is_ajax():
                return HttpResponse('OK')
    else:
        form = EditPersonForm(instance=person)
    return render(request, 'hello/edit.html', {'form': form,  'pk': pk, 'person': person})
