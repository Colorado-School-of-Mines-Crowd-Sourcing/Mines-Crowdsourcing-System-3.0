from django.shortcuts import render, redirect
from django.contrib import messages
from django.apps import apps
from django.http import Http404

from participant.models import User, Task, Tag
from .forms import CreateTask, CreateApproval

# TODO: Remove random import when user authentication is done
import random, string

# Logger
import logging

logger = logging.getLogger(__name__)
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form_task = CreateTask(request.POST)
        # check whether it's valid
        if form_task.is_valid() :
            # Task creation
            new_task = form_task.save(commit=False)
            new_task.requester = request.user
            new_task.save()

            # Tag creation
            for tag in request.POST.get('tags').split(','):
                logger.info(request, 'tag ', tag, ' created')
                new_tag = Tag.create(tag, new_task)
                new_tag.save()

            messages.success(request, 'Your task has been submitted for review.')
            return redirect('requester_create')

    # if a GET (or any other method) we'll create a blank form
    else:
        form_task = CreateTask()
    return render(request, 'requester/create.html', {'form_task': form_task})

def see_tasks(request):
    user = request.user
    if user.is_anonymous:
        return render(request, 'requester/tasks.html')
    else:
        pending = Task.objects.filter(
            requester = user,
            status = Task.PENDING,
        )

        active = Task.objects.filter(
            requester = user,
            status = Task.ACTIVE,
        )

        completed = Task.objects.filter(
            requester = user,
            status = Task.COMPLETED,
        )

        return render(request, 'requester/tasks.html', {
            'pending': pending,
            'active': active,
            'completed': completed,
        })


def approve_contributors(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
        if task.requester != request.user:
            raise Task.DoesNotExist

        if request.method == 'POST':
            form_approval = CreateApproval(request.POST, task.participants)
            if form_approval.is_valid() :
                users = form_approval.participants
                for user in users:
                    if user not in task.approved_contributors:
                        user.reward_balance += task.reward_amount
                        task.approved_contributors.add(user)
                task.save()
                messages.success(request, 'Your task has been submitted for review.')
                return redirect('contributor_approval', task_id)
        else:
            form_approval = CreateTask(task.participants)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
        
    return render(request, 'requester/approval.html',
                {'form_approval': form_approval,
                'task': task})
