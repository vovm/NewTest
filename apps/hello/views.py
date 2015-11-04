import json
import signals
from time import strftime

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import About, AllRequest
from .forms import EditPersonForm, EditRequestForm


def all_people(request):
    people = About.objects.order_by('id')[:1]
    return render(request, 'hello/about.html', {'people': people})


def request_list(request):
    requests = AllRequest.objects.order_by('-date')[:10]
    return render(request, 'hello/request.html', {'requests': requests})


@csrf_exempt
def ajax_request_list(request):
    requests = AllRequest.objects.order_by('-date')[:10]
    data = [{'req_id': req.id, 
             'req_date': req.date.strftime("%d/%b/%Y %H:%M:%S"), 
             'req_method': req.method,
             'req_path': req.path, 
             'req_priority': req.priority} for req in requests]
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


def request_list_priority(request, rank):
    if rank == "low":
        priority = 0
    elif rank == "high":
        priority = 1
    else:
        priority = 0
        rank = 'low'
    requests_list = AllRequest.objects.order_by('-id').filter(priority=priority)
    paginator = Paginator(requests_list, 10)
    page = request.GET.get('page')
    try:
        requests = paginator.page(page)
    except:
        requests = paginator.page(1)
    return render(request, 'hello/request_priority.html', {'requests': requests, 'rank': rank})


def edit_request(request, pk):
    req = get_object_or_404(AllRequest, pk=pk)
    if request.method == "POST":
        form = EditRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('request_list'))
    else:
        form = EditRequestForm(instance=req)
    return render(request, 'hello/edit_request.html', {'form': form,  'pk': pk, 'req': req})
