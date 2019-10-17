from django.shortcuts import render
from participant.models import *
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
