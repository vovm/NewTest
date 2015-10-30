import json
from time import strftime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import About, AllRequest

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
