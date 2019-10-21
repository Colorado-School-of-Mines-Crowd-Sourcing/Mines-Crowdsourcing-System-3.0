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
        return render(request, 'participant/completed_task.html')
    else:
        completed_tasks_participant = ParticipantCompletedTask.objects.filter(
            user=user
        )
        return render(request, 'participant/completed_task.html', {
            'completed_tasks_participant': completed_tasks_participant})


def search_results(request):
    query = request.GET.get('q')
    query_title = Task.objects.filter(Q(title__contains=query), is_posted=True)
    query_tag = Task.objects.filter(Q(tag__tag=query), is_posted=True)
    query_result = query_tag.union(query_title)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result})
