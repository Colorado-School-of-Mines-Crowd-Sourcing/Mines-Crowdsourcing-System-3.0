from django.shortcuts import render
from participant.models import *
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.http import HttpResponse


def index(request):
    return render(request, 'participant/index.html')


def all_available_tasks(request):
    return render(request, 'participant/all_tasks.html', {
        'all_tasks': Task.objects.filter(is_posted=True)})


def completed_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'participant/completed_tasks.html')
    else:
        completed_tasks = Task.objects.filter(
            participantcompletedtask__user=user
        )
        return render(request, 'participant/completed_tasks.html', {
            'completed_tasks': completed_tasks})


def search_results(request):
    query = request.GET.get('q')
    query_title = Task.objects.filter(Q(title__contains=query), is_posted=True)
    query_tag = Task.objects.filter(Q(tag__tag=query), is_posted=True)
    query_result = query_tag.union(query_title)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result})
