from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from participant.models import *
from django.db.models import Q
from django.http import Http404
from django.contrib import messages


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
        all_completed_tasks = Task.objects.filter(
            participantcompletedtask__user=user
        )
        return render(request, 'participant/completed_tasks.html', {
            'completed_tasks': all_completed_tasks})


def search_results(request):
    query = request.GET.get('q')
    query_title = Task.objects.filter(Q(title__contains=query), is_posted=True)
    query_tag = Task.objects.filter(Q(tag__tag__contains=query), is_posted=True)
    query_result = query_tag.union(query_title)
    return render(request, 'participant/search_result.html', {
        'resulted_tasks': query_result})


def task_details(request, task_id):
    try:
        current_task = Task.objects.get(is_posted=True, pk=task_id)
        already_completed = False
        if request.method == 'POST':
            ParticipantCompletedTask.create(request.user, current_task).save()
            messages.success(request, 'Thank you for contribution! This task has been marked complete and is waiting '
                                      'for the approval of the requester.')
        try:
            ParticipantCompletedTask.objects.get(task=current_task)
            already_completed = True
        except ObjectDoesNotExist:
            pass
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    return render(request, 'participant/task_details.html', {'task': current_task,
                                                             'already_completed': already_completed})
