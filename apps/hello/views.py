from django.shortcuts import render

from .models import About


def all_people(request):
    people = About.objects.order_by('id')[:1]
    return render(request, 'hello/about.html', {'people': people})
